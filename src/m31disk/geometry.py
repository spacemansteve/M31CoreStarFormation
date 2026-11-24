"""PT03 orbital geometry. Positions in pc, velocities in km/s, angles in radians."""
import numpy as np


def kepler(mean, ecc):
    """Solve for E on [-pi, pi] by monotone bisection for elliptic orbits."""
    mean, ecc = np.broadcast_arrays(mean, ecc)
    if not np.all(np.isfinite(mean) & (ecc >= 0) & (ecc < 1)):
        raise ValueError("Elliptic orbits require finite M and 0 <= e < 1")
    mean = (mean + np.pi) % (2 * np.pi) - np.pi
    lo, hi = mean - ecc, mean + ecc
    for _ in range(54):
        mid = (lo + hi) / 2
        below = mid - ecc * np.sin(mid) < mean
        lo, hi = np.where(below, mid, lo), np.where(below, hi, mid)
    return (lo + hi) / 2


def orbit(a, ecc, mean, mu):
    """Position and velocity in the orbital frame for mu = G M in pc (km/s)^2."""
    a, ecc, mean = np.broadcast_arrays(a, ecc, mean)
    if not np.all(np.isfinite(a) & (a > 0)) or not (np.isfinite(mu) and mu > 0):
        raise ValueError("Positive finite a and mu required")
    anomaly = kepler(mean, ecc)
    c, s = np.cos(anomaly), np.sin(anomaly)
    b = np.sqrt((1 - ecc) * (1 + ecc))
    zeros = np.zeros_like(c)
    position = a[..., None] * np.stack((c - ecc, b * s, zeros), axis=-1)
    speed = np.sqrt(mu / a) / (1 - ecc * c)
    velocity = speed[..., None] * np.stack((-s, b * c, zeros), axis=-1)
    return position, velocity


def rotation(node, incline, apsis):
    """Active Rz(node) Rx(incline) Rz(apsis) for one or many orbits."""
    n, i, w = np.broadcast_arrays(node, incline, apsis)
    cn, ci, cw = np.cos(n), np.cos(i), np.cos(w)
    sn, si, sw = np.sin(n), np.sin(i), np.sin(w)
    rows = ((cn*cw - sn*ci*sw, -cn*sw - sn*ci*cw, sn*si),
            (sn*cw + cn*ci*sw, -sn*sw + cn*ci*cw, -cn*si),
            (si*sw, si*cw, ci))
    return np.stack([np.stack(row, axis=-1) for row in rows], axis=-2)


def precession(position, omega):
    """Rigid velocity around the disk z axis, omega in km/s/pc."""
    x, y, z = np.moveaxis(position, -1, 0)
    return omega * np.stack((-y, x, np.zeros_like(z)), axis=-1)


def project(position, velocity, angles, omega):
    """Disk to sky, X west, Y north, +Z toward observer, LOS receding positive."""
    matrix = rotation(*angles)
    sky = position @ matrix.T
    moved = (velocity + precession(position, omega)) @ matrix.T
    return sky[:, :2], -moved[:, 2]


def toy_disk(seed, count=10_000):
    """Toy aligned eccentric orbits with modest thickness, equal luminosities."""
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.5, 3, count)
    ecc = rng.uniform(0.15, 0.5, count)
    pos, vel = orbit(a, ecc, rng.uniform(-np.pi, np.pi, count), mu=430_000.)
    node = rng.uniform(-np.pi, np.pi, count)
    tilt = rng.rayleigh(np.deg2rad(5), count)
    apsis = rng.normal(0, np.deg2rad(12), count) - node
    matrix = rotation(node, tilt, apsis)
    return (matrix @ pos[..., None])[..., 0], (matrix @ vel[..., None])[..., 0]
