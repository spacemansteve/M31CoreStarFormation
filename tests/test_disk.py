import unittest

import numpy as np
from numpy.testing import assert_allclose
from scipy.ndimage import gaussian_filter

from m31disk.geometry import kepler, orbit, precession, project, rotation
from m31disk.moments import EDGES, PSF_SIGMA_PIX, maps


class Geometry(unittest.TestCase):
    def test_kepler_and_conservation(self):
        mean = np.linspace(-3, 3, 301)
        for e in (0., 0.4, 0.99):
            E = kepler(mean, e)
            assert_allclose(E - e*np.sin(E), mean, atol=2e-15, rtol=0)
            r, v = orbit(2., e, mean, 8.)
            energy = (v*v).sum(axis=1)/2 - 8/np.linalg.norm(r, axis=1)
            assert_allclose(energy, -2., atol=2e-11, rtol=0)
            h = np.cross(r, v)
            assert_allclose(h[:, 2], np.sqrt(16*(1-e**2)), atol=2e-12)
            assert_allclose(h[:, :2], 0.)

    def test_apsides_and_circle(self):
        for e in (0., .5):
            r, v = orbit(2., e, [0., np.pi], 8.)
            assert_allclose(r[:, 0], [2*(1-e), -2*(1+e)])
            ratio = np.sqrt((1+e)/(1-e))
            assert_allclose(v[:, 1], [2*ratio, -2/ratio])
            assert_allclose(v[:, 0], 0., atol=1e-14)

    def test_rotation_and_sign(self):
        mat = rotation(-.3, .7, 1.)
        assert_allclose(mat.T @ mat, np.eye(3), atol=1e-15)
        self.assertAlmostEqual(np.linalg.det(mat), 1.)
        q = np.pi/2
        assert_allclose(rotation(q, q, q) @ [1., 0., 0.], [0, 0, 1], atol=1e-15)
        xy, los = project(np.array([[1., 0., 0.]]), np.array([[0., 1., 0.]]),
                          (q, q, 0.), 0.)
        assert_allclose(xy, [[0., 1.]], atol=1e-15)
        assert_allclose(los, [-1.])

    def test_precession(self):
        r = np.array([(x, y, 2) for x in (-1, 0, 1) for y in (-1, 0, 1)])
        for speed in (-3., 0., 3.):
            expected = np.cross(np.array([0., 0., speed]), r)
            assert_allclose(precession(r, speed), expected)


class Moments(unittest.TestCase):
    def test_against_smoothing_velocity_channels(self):
        xy = np.array([[0.04, 0.04], [.04, .04], [.18, .04], [-4.8, .04]])
        los = np.array([-10., -10., 20., 20.])
        flux, v, s = maps(xy, los, 2)
        channels = []
        for speed in (-10., 20.):
            y, x = xy[los == speed].T[::-1]
            hist = np.histogram2d(y, x, (EDGES, EDGES))[0]
            blurred = gaussian_filter(hist, PSF_SIGMA_PIX, mode="constant")
            channels.append(blurred.reshape(44, 2, 44, 2).sum(axis=(1, 3)))
        low, high = channels
        used = flux > 1e-8
        assert_allclose(flux.sum(), len(los), atol=1e-13)
        assert_allclose(flux, low + high, atol=1e-14)
        p = high[used] / flux[used]
        assert_allclose(v[used], -10 + 30*p, atol=1e-12)
        # Two-point distribution: var = p(1-p)(v2-v1)^2.
        assert_allclose(s[used], 30*np.sqrt(np.maximum(p*(1-p), 0)), atol=2e-6)
