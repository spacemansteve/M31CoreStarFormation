"""Equal-light particle LOSVD moments on a padded, fixed physical grid."""
import numpy as np
from scipy.ndimage import gaussian_filter

PIXEL_PC = 0.125
EDGES = np.linspace(-5.5, 5.5, 89)
PSF_SIGMA_PIX = 1.2


def maps(xy, los, bin_factor):
    """Deposit F, Fv, Fv², blur spatially, sum into bins, then normalize."""
    if np.any(np.abs(xy) >= 4.875):
        # A 5-pixel margin holds the full truncated kernel.
        raise ValueError("Particles exceed the padded model footprint")
    if bin_factor < 1 or (len(EDGES) - 1) % bin_factor:
        raise ValueError("Bin factor must divide the map width")
    planes = []
    for weight in (None, los, los**2):
        plane = np.histogram2d(xy[:, 1], xy[:, 0], (EDGES, EDGES), weights=weight)[0]
        plane = gaussian_filter(plane, PSF_SIGMA_PIX, mode="constant", truncate=4.)
        bins = len(plane) // bin_factor
        planes.append(plane.reshape(bins, bin_factor, bins, bin_factor).sum(axis=(1, 3)))
    flux, first, second = planes
    divisor = np.where(flux > 0, flux, np.nan)
    mean = first / divisor
    dispersion = np.sqrt(np.maximum(0, second / divisor - mean**2))
    return flux, mean, dispersion
