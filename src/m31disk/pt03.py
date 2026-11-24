"""Independent draw of the PT03 Table 1 non-aligned disk (§§2.3, 3.1)."""
import numpy as np
from scipy.special import expit

from .geometry import orbit, project, rotation

PC_PER_ARCSEC = 3.73
MU = 4.30091727e-3 * 1.02e8  # pc (km/s)^2
ANGLES = np.deg2rad([-42.8, 54.1, -34.5])  # node, inclination, apsis


def sample_elements(rng, size):
    # Eq. 17: a Sigma(a) is Gamma(shape=4, scale=a0) times a Fermi cutoff.
    if size <= 0:
        raise ValueError("Expected a positive particle count")
    pieces = []
    needed = size
    while needed:
        proposal = rng.gamma(4, 1.37, needed * 3)
        accepted = proposal[rng.random(len(proposal)) < expit(4*(4.24-proposal))]
        pieces.append(accepted[:needed])
        needed -= len(pieces[-1])
    a = np.concatenate(pieces)
    em = .197 * (4.45-a) * np.exp(-.5*((a-1.71)/1.52)**2)
    sigma_i = np.deg2rad(24.6) * np.exp(-a/31.5)
    ex = rng.normal(em, .307)
    ey = rng.normal(0, .307, size)
    initially_bound = np.hypot(ex, ey) < 1
    pending = np.flatnonzero(~initially_bound)
    while pending.size:
        ex[pending] = rng.normal(em[pending], .307)
        ey[pending] = rng.normal(0, .307, pending.size)
        pending = pending[np.hypot(ex[pending], ey[pending]) >= 1]
    tilt = np.empty(size)
    pending = np.arange(size)
    while pending.size:
        # Rayleigh proposal supplies I exp(-I²/2s²). Correct I to sin(I).
        trial = rng.rayleigh(sigma_i[pending])
        tilt[pending] = trial
        keep = (trial < np.pi) & (rng.random(len(trial)) < np.sinc(trial/np.pi))
        pending = pending[~keep]
    node, phase = rng.uniform(0, 2*np.pi, (2, size))
    return a, ex, ey, tilt, node, phase, initially_bound


def sample_sky(rng, size):
    a, ex, ey, tilt, node, phase, initially_bound = sample_elements(rng, size)
    pos, vel = orbit(a, np.hypot(ex, ey), phase, MU)
    orient = rotation(node, tilt, np.arctan2(ey, ex)-node)
    pos = (orient @ pos[..., None])[..., 0]
    vel = (orient @ vel[..., None])[..., 0]
    xy, los = project(pos, vel, ANGLES, omega=0)
    return xy / PC_PER_ARCSEC, los, initially_bound
