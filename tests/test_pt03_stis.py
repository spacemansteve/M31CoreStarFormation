import unittest

import numpy as np
from numpy.testing import assert_allclose
from scipy.integrate import quad, dblquad
from scipy.special import eval_hermite
from scipy.stats import ncx2

from m31disk.pt03 import sample_elements
from m31disk.stis import (Aperture, PSF_STEP, VELOCITY, fit_profile, inferred_edges,
                          psf, slit_coordinates)


class Distribution(unittest.TestCase):
    def test_orbital_element_laws(self):
        # Test empirical probabilities against independent quadrature, using
        # five binomial standard errors for this fixed 50k draw.
        n = 50_000
        a, ex, ey, inc, node, phase, initially_bound = sample_elements(np.random.default_rng(938), n)
        def radial(x):
            return x**3 * np.exp(-x/1.37) / (1 + np.exp(4*(x-4.24)))
        norm = quad(radial, 0, 25)[0]
        def probability(check, expected):
            prob = np.mean(expected)
            self.assertLess(abs(np.mean(check)-prob), 5*np.sqrt(prob*(1-prob)/n))
        for t in (1.5, 3.5, 4.5):
            probability(a < t, quad(radial, 0, t)[0]/norm)
        e = np.hypot(ex, ey)
        self.assertLess(e.max(), 1)
        mean_e = .197*(4.45-a)*np.exp(-.5*((a-1.71)/1.52)**2)
        noncentrality = (mean_e/.307)**2
        conditional = ncx2.cdf((.5/.307)**2, 2, noncentrality) / ncx2.cdf((1/.307)**2, 2, noncentrality)
        probability(e < .5, conditional)
        probability(initially_bound, ncx2.cdf((1/.307)**2, 2, noncentrality))
        self.assertGreater(ex[a < 2].mean(), .35)
        self.assertLess(abs(ey.mean()), .01)
        def tilted_radial(x, max_i):
            width = np.deg2rad(24.6)*np.exp(-x/31.5)
            def law(i):
                return np.sin(i)*np.exp(-.5*(i/width)**2)
            return radial(x) * quad(law, 0, max_i)[0] / quad(law, 0, np.pi)[0]
        probability(inc < .5, quad(tilted_radial, 0, 15, args=(.5,))[0]/norm)
        for angle in (phase, node, phase-node):
            self.assertLess(abs(np.exp(1j*angle).mean()), .02)


class Spectroscopy(unittest.TestCase):
    def test_geometry(self):
        theta = np.deg2rad(39)
        directions = np.array([[-np.sin(theta), np.cos(theta)], [np.cos(theta), np.sin(theta)]])
        along, across = slit_coordinates(directions)
        assert_allclose(along, [1, 0], atol=1e-15)
        assert_allclose(across, [0, 1], atol=1e-15)
        assert_allclose(inferred_edges([-.1, 0, .2]), [-.15, -.05, .1, .3])

    def test_slit_throughput(self):
        def intensity(r):
            return 1.01*np.exp(-.5*(r/.0329)**2) + .12*np.exp(-.5*((r-.105)/.0384)**2)
        total = quad(lambda r: 2*np.pi*r*intensity(r), 0, 1)[0]
        aperture = Aperture(-.037, .061, psf(PSF_STEP), PSF_STEP)
        for x, y in ((0, 0), (.071, -.033), (.18, .08)):
            exact = dblquad(lambda t, s: intensity(np.hypot(s-x, t-y)),
                            -.037, .061, -.05, .05)[0]/total
            _, weights = aperture.weights(np.array([x]), np.array([y]))
            assert_allclose(weights[0], exact, atol=.0008, rtol=0)
        # Integrated point-source response across the sky equals geometric area.
        assert_allclose(aperture.response.sum() * PSF_STEP**2, .098*.1, atol=1e-12)

    def test_line_estimators(self):
        center, sigma = -147., 103.
        y = (VELOCITY-center)/sigma
        for method, h3, h4 in (("FQ", 0., 0.), ("FCQ", -.08, .12)):
            shape = 1 + h3*eval_hermite(3, y)/np.sqrt(48) + h4*eval_hermite(4, y)/np.sqrt(384)
            histogram = np.r_[0, np.exp(-y*y/2)*shape, 0]
            expected = [center, sigma] if method=="FQ" else [center, sigma, h3, h4]
            assert_allclose(fit_profile(histogram, method), expected, atol=1e-7)
