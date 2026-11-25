"""Predict the Bender red-STIS profiles at fixed PT03 Table 1 parameters."""
import csv
from pathlib import Path
from time import perf_counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from m31disk.pt03 import sample_sky
from m31disk.stis import (Aperture, PSF_STEP, VELOCITY_EDGES, fit_profile, histogram,
                          inferred_edges, psf, slit_coordinates)

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (7101, 7102, 7103, 7104)
BATCH = 50_000
BATCHES_PER_SEED = 5
FIELDS = ("v_kms", "sigma_kms", "h3", "h4")
VARIANTS = ("baseline", "slit_nw", "slit_se", "single_pixel", "discard_orbit",
            "archive_pa", "archive_p3_ne", "archive_p3_sw", "archive_native_pixel")
ARCHIVE_PA = 38.97643
ARCHIVE_PIXEL = .050809


def make_apertures(rows):
    step = PSF_STEP
    kernel = psf(step)
    baseline, single, native = [], [], []
    for method in ("FQ", "FCQ"):
        centers = np.array([float(r["radius_arcsec"]) for r in rows if r["method"] == method])
        edges = inferred_edges(centers)
        baseline.extend(Aperture(a, b, kernel, step) for a, b in zip(edges[:-1], edges[1:]))
        single.extend(Aperture(c-.0255, c+.0255, kernel, step) for c in centers)
        native.extend(Aperture(c-ARCHIVE_PIXEL/2, c+ARCHIVE_PIXEL/2, kernel, step)
                      for c in centers)
    return baseline, single, native


def simulate(rows):
    apertures, single, native = make_apertures(rows)
    windows_by_variant = (apertures, apertures, apertures, single, apertures,
                          apertures, apertures, apertures, native)
    shape = (len(SEEDS), len(VARIANTS), len(rows))
    hist = np.zeros((*shape, len(VELOCITY_EDGES)+1))
    squared = np.zeros(shape)
    first_rejected = 0
    for g, seed in enumerate(SEEDS):
        rng = np.random.default_rng(seed)
        for _ in range(BATCHES_PER_SEED):
            xy, los, initially_bound = sample_sky(rng, BATCH)
            first_rejected += np.count_nonzero(~initially_bound)
            nominal = slit_coordinates(xy)
            archive = slit_coordinates(xy, ARCHIVE_PA)
            velocity_index = np.searchsorted(VELOCITY_EDGES, los, side="right")
            for j, (variant, windows) in enumerate(zip(VARIANTS, windows_by_variant)):
                along, across = archive if variant.startswith("archive_") else nominal
                cross_offset = {"slit_nw": .025, "slit_se": -.025}.get(variant, 0.)
                along_offset = {"archive_p3_ne": ARCHIVE_PIXEL/2,
                                "archive_p3_sw": -ARCHIVE_PIXEL/2}.get(variant, 0.)
                keep = np.abs(across) < .45
                if variant == "discard_orbit":
                    keep &= initially_bound
                location = along[keep] - along_offset
                relative = across[keep] - cross_offset
                channel = velocity_index[keep]
                for k, window in enumerate(windows):
                    counts, squares = histogram(window, location, relative, channel)
                    hist[g, j, k] += counts
                    squared[g, j, k] += squares
    print(f"Initial unbound eccentricities: {first_rejected:,}")
    return hist, squared


def measure(rows, hist, squared):
    records = []
    for j, variant in enumerate(VARIANTS):
        for k, row in enumerate(rows):
            method = row["method"]
            groups = hist[:, j, k]
            total = groups.sum(axis=0)
            model = fit_profile(total, method)
            flux = total.sum()
            record = dict(variant=variant, method=method, radius_arcsec=row["radius_arcsec"],
                          light=flux, n_eff=flux**2/squared[:, j, k].sum(),
                          outside_velocity_fraction=(total[0]+total[-1])/flux)
            if variant == "baseline":
                # Between independent draws, and change on doubling the draw.
                separate = np.array([fit_profile(group, method) for group in groups])
                scatter = separate.std(axis=0, ddof=1) / np.sqrt(len(groups))
                half = fit_profile(groups[:len(groups)//2].sum(axis=0), method)
            for i, field in enumerate(FIELDS[:len(model)]):
                record[field] = model[i]
                record["delta_"+field] = model[i] - float(row[field])
                if variant == "baseline":
                    record["mc_se_"+field] = scatter[i]
                    record["half_shift_"+field] = model[i] - half[i]
            records.append(record)
    return records


def plot(rows, records):
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, layout="constrained")
    for ax, field, error, label in zip(axes.flat, FIELDS,
            ("v_error_kms", "sigma_error_kms", "h3_error", "h4_error"),
            ("LOS velocity (km/s)", "Dispersion (km/s)", "h₃", "h₄")):
        ax.axvline(0, color=".8", lw=.8)
        for method, color, marker in (("FQ", "#ac5700", "s"), ("FCQ", "#16528e", "o")):
            obs = [r for r in rows if r["method"] == method and r[field]]
            if not obs:
                continue
            radius = np.array([float(r["radius_arcsec"]) for r in obs])
            ax.errorbar(radius, [float(r[field]) for r in obs], [float(r[error]) for r in obs],
                        fmt=marker, markersize=3, fillstyle="none", color=color,
                        elinewidth=.8, label=f"STIS {method}")
            model = [r for r in records if r["method"]==method and r["variant"]=="baseline"]
            ax.plot(radius, [r[field] for r in model], color=color,
                    ls="--" if method=="FQ" else "-", label=f"PT03 {method} proxy")
        ax.set_ylabel(label)
    axes[0, 0].legend(fontsize=8, ncol=2)
    for ax in axes[1]:
        ax.set_xlabel("Slit radius (arcsec, positive toward P1)")
    fig.suptitle("Approximate independent reconstruction · PT03 non-aligned disk and HST/STIS")
    fig.savefig(ROOT / "figures/pt03_stis.png", dpi=170)
    plt.close(fig)


def main():
    start = perf_counter()
    with (ROOT / "docs/bender_reference.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    # The source table is ordered by method then increasing reported radius.
    if [r["method"] for r in rows] != ["FQ"]*25 + ["FCQ"]*22:
        raise ValueError("Unexpected STIS reference table layout")
    hist, squared = simulate(rows)
    records = measure(rows, hist, squared)
    fields = list(dict.fromkeys(key for row in records for key in row))
    with (ROOT / "docs/pt03_stis_profiles.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fields, lineterminator="\n")
        writer.writeheader()
        for row in records:
            writer.writerow({k: f"{v:.8g}" if isinstance(v, float) else v for k, v in row.items()})
    plot(rows, records)
    print(f"{len(rows)} apertures, {len(VARIANTS)} scenarios, {len(SEEDS)*BATCH*BATCHES_PER_SEED:,} particles in {perf_counter()-start:.1f} s")


if __name__ == "__main__":
    main()
