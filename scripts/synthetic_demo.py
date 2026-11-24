"""Run the bounded Stage 1 injection experiment from the repository root."""
import csv
import resource
import sys
from itertools import product
from pathlib import Path
from time import perf_counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from m31disk.geometry import project, toy_disk
from m31disk.moments import maps

ANGLES = (24, 55, -20)  # degrees, arbitrary toy truth
GRID = np.arange(-24, 25, 2)
NOISE = 8.  # km/s per retained bin


def observe(disk, degrees, omega, factor):
    """Independent scalar expansion of the disk-to-sky and LOS equations."""
    n, i, a = np.deg2rad(degrees)
    x, y, z = disk[0].T
    vx, vy, vz = disk[1].T
    u = np.cos(a)*x - np.sin(a)*y
    t = np.cos(i)*(np.sin(a)*x + np.cos(a)*y) - np.sin(i)*z
    xy = np.column_stack((np.cos(n)*u - np.sin(n)*t, np.sin(n)*u + np.cos(n)*t))
    los = -(np.sin(i)*(np.sin(a)*vx + np.cos(a)*vy + omega*u) + np.cos(i)*vz)
    return maps(xy, los, factor)


def predict(disk, degrees, omega, factor):
    return maps(*project(*disk, np.deg2rad(degrees), omega), factor)


def speed_fit(model, degrees, factor, observed, noise):
    flux, truth, _ = observed
    model_flux, baseline, _ = predict(model, degrees, 0, factor)
    _, offset, _ = predict(model, degrees, 16, factor)
    # Mean LOS velocity is affine in omega for fixed PSF and geometry.
    used = (flux >= 12) & (model_flux >= 12)
    data = truth[used] + noise[used]
    slopes = (offset[used] - baseline[used]) / 16
    estimate = baseline[used] + GRID[:, None]*slopes
    score = np.sum(((data - estimate)/NOISE)**2, axis=1)
    flat = np.ptp(score) < 1e-8
    best = None if flat else int(GRID[np.argmin(score)])
    return best, used.sum(), score


def main():
    start = perf_counter()
    rows = []
    for seed, factor, injected in product((21, 32, 43), (2, 4), (-12, 0, 12)):
        disk = toy_disk(seed)
        obs = observe(disk, ANGLES, injected, factor)
        noise = np.random.default_rng(seed + 90*factor).normal(0, NOISE, obs[0].shape)
        for draw, count in (("shared", 10000), ("independent", 10000), ("independent", 40000)):
            model = disk if draw == "shared" else toy_disk(seed+1000, count)
            best, bins, _ = speed_fit(model, ANGLES, factor, obs, noise)
            if best is None:
                raise RuntimeError("Inclined disk produced a flat objective")
            rows.append((seed, factor, injected, draw, count, best, bins))
        best, _, _ = speed_fit(disk, ANGLES, factor, obs, np.zeros_like(noise))
        if best != injected:
            raise RuntimeError("Noiseless conditional injection failed")

    # Simultaneous angle and speed recovery on a small discrete grid. Use the
    # same central high-light bins for every candidate and reject missing bins.
    disk = toy_disk(21)
    obs = observe(disk, ANGLES, 12, 4)
    used = obs[0] > 150
    rng = np.random.default_rng(944)
    data = obs[1][used] + rng.normal(0, NOISE, used.sum())
    trials = []
    clean_trials = []
    for angles in product((16, 24, 32), (47, 55, 63), (-30, -20, -10)):
        _, v, _ = predict(disk, angles, 0, 4)
        _, shifted, _ = predict(disk, angles, 16, 4)
        pred = v[used] + GRID[:, None]*(shifted[used] - v[used])/16
        scores = np.sum(((data - pred)/NOISE)**2, axis=1)
        scores[~np.isfinite(scores)] = np.inf
        trials.append((scores.min(), angles, GRID[scores.argmin()]))
        clean_scores = np.sum(((obs[1][used] - pred)/NOISE)**2, axis=1)
        clean_scores[~np.isfinite(clean_scores)] = np.inf
        clean_trials.append((clean_scores.min(), angles, GRID[clean_scores.argmin()]))
        if angles == ANGLES:
            print("Joint noisy score at injected parameters:", scores[GRID == 12].item())
    clean_score, clean_angles, clean_speed = min(clean_trials)
    if (clean_angles, clean_speed) != (ANGLES, 12) or clean_score > 1e-15:
        raise RuntimeError("Noiseless joint recovery failed")
    print("Joint noiseless minimum:", min(clean_trials))
    print("Joint noisy shared-draw minimum (score, angles deg, omega):", min(trials), "bins:", used.sum())
    face = observe(disk, (24, 0, -20), 12, 2)
    best, _, score = speed_fit(disk, (24, 0, -20), 2, face, np.zeros_like(face[0]))
    if best is not None:
        raise RuntimeError("Face-on pattern speed must be unidentifiable")
    print("Face-on grid score range:", np.ptp(score))
    with Path("docs/synthetic_recovery.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("seed", "bin_factor", "injected_kms_pc", "model_draw",
                         "model_particles", "recovered_kms_pc", "retained_bins"))
        writer.writerows(rows)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), sharex=True, sharey=True, layout="constrained")
    for ax, array, title, cmap in zip(axes, obs, ("Light (particles/bin)", "Mean LOS (km/s)", "LOS dispersion (km/s)"),
                                     ("magma", "RdBu_r", "viridis")):
        field = np.where(obs[0] >= 12, array, np.nan)
        limit = np.nanmax(np.abs(field))
        im = ax.imshow(field, origin="lower", extent=(-5.5,5.5,-5.5,5.5), cmap=cmap,
                       vmin=-limit if cmap=="RdBu_r" else 0, vmax=limit, interpolation="nearest")
        ax.set(xlim=(-4.5,4.5), ylim=(-4.5,4.5), xlabel="West (pc)", title=title)
        fig.colorbar(im, ax=ax, shrink=.7)
    axes[0].set_ylabel("North (pc)")
    fig.suptitle("SYNTHETIC TEST  •  eccentric disk with injected Ω = +12 km/s/pc")
    fig.savefig("figures/synthetic_disk.png", dpi=160)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_mib = rss / (1024**2 if sys.platform == "darwin" else 1024)
    print(f"Suite wall time {perf_counter()-start:.2f} s, peak process RSS {rss_mib:.1f} MiB")


if __name__ == "__main__":
    main()
