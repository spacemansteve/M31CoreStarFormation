"""STIS rectangular aperture response and unweighted PT03 Eq. 19 LOSVD fits."""
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.optimize import least_squares
from scipy.signal import fftconvolve

VELOCITY_EDGES = np.arange(-4002.5, 4003, 5.)
VELOCITY = (VELOCITY_EDGES[1:] + VELOCITY_EDGES[:-1])/2
SLIT_WIDTH = .1
PSF_STEP = .0025


def slit_coordinates(xy, pa_deg=39.):
    """Positive along-slit points to P1 (NE), positive across-slit to NW."""
    pa = np.deg2rad(pa_deg)
    west, north = xy.T
    return -west*np.sin(pa) + north*np.cos(pa), west*np.cos(pa) + north*np.sin(pa)


def inferred_edges(centers):
    """Midpoints between neighboring centers, half-spacing extrapolation at ends."""
    gaps = np.diff(centers)
    if len(gaps) == 0 or np.any(gaps <= 0):
        raise ValueError("Expected multiple increasing bin centers")
    return np.r_[centers[0]-gaps[0]/2, centers[:-1]+gaps/2, centers[-1]+gaps[-1]/2]


def psf(step):
    """Midpoint quadrature of the circular PT03 Eq. 21 intensity per sky area."""
    support = int(np.ceil(.35/step))
    axis = np.arange(-support, support+1)*step
    r = np.hypot(axis[:, None], axis)
    values = 1.01*np.exp(-.5*(r/.0329)**2) + .12*np.exp(-.5*((r-.105)/.0384)**2)
    return values / values.sum()


class Aperture:
    """Fraction of light entering one rectangular extraction after spatial blur."""
    def __init__(self, low, high, kernel, step):
        self.step = step
        self.center = (high + low)/2
        half = (high - low)/2
        # Fractional area of each cell in the rectangle before convolution.
        def interval(half_width):
            axis = np.arange(-np.ceil(half_width/step), np.ceil(half_width/step)+1)*step
            overlap = np.minimum(axis+step/2, half_width)-np.maximum(axis-step/2, -half_width)
            return np.maximum(0, overlap)/step

        rect = np.outer(interval(SLIT_WIDTH/2), interval(half))
        self.response = fftconvolve(rect, kernel, mode="full").clip(0, 1)
        self.cy, self.cx = (np.array(self.response.shape)-1)/2

    def weights(self, along, across):
        x = (along-self.center)/self.step + self.cx
        y = across/self.step + self.cy
        inside = (x >= 0) & (x <= 2*self.cx) & (y >= 0) & (y <= 2*self.cy)
        w = map_coordinates(self.response, [y[inside], x[inside]], order=1)
        return inside, w


def histogram(aperture, along, across, velocity_index):
    inside, w = aperture.weights(along, across)
    # Index 0 and the last index are under/overflow, preserved for auditing.
    hist = np.bincount(velocity_index[inside], weights=w, minlength=len(VELOCITY)+2)
    return hist, np.sum(w*w)


def losvd_shape(v, center, sigma, h3=0., h4=0.):
    y = (v-center)/sigma
    h_3 = (2*y**3-3*y)/np.sqrt(3)
    h_4 = (4*y**4-12*y*y+3)/np.sqrt(24)
    return np.exp(-.5*y*y)*(1 + h3*h_3 + h4*h_4)


def fit_profile(hist, method):
    """FQ proxy: Gaussian. FCQ proxy: fourth-order Gauss–Hermite (free amplitude)."""
    if method not in ("FQ", "FCQ"):
        raise ValueError("Unknown measurement method")
    density = hist[1:-1]
    if density.sum() <= 0:
        raise ValueError("Empty LOSVD")
    density = density / density.max()
    mean = np.average(VELOCITY, weights=density)
    sigma = np.sqrt(np.average((VELOCITY-mean)**2, weights=density))
    initial = [1., mean, sigma]
    lower = [0., VELOCITY[0], 2.5]
    upper = [np.inf, VELOCITY[-1], 4000.]
    if method == "FCQ":
        initial += [0., 0.]
        lower += [-np.inf, -np.inf]
        upper += [np.inf, np.inf]

    def residual(params):
        amp, center, spread, *hermite = params
        return amp*losvd_shape(VELOCITY, center, spread, *hermite) - density

    result = least_squares(residual, initial, bounds=(lower, upper), x_scale="jac",
                           ftol=1e-8, xtol=1e-8, gtol=1e-8)
    if not result.success or result.active_mask.any():
        raise RuntimeError("LOSVD fit failed or reached a numerical boundary")
    return result.x[1:]
