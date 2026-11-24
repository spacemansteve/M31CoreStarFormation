"""Restore one MAST association if requested and render its central six arcsec."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import AsinhNorm
import numpy as np
from scipy.ndimage import map_coordinates

ROOT = Path(__file__).resolve().parents[1]
FILE = "j9am01010_drz.fits"
URI = "mast:HST/product/" + FILE
URL = "https://mast.stsci.edu/api/v0.1/Download/file?uri=" + URI
SIZE = 16030080
DIGEST = "78549f5577afa5818917133141aa17d807ec279f6902cf5beab6b53fe24b74a4"


def check(data):
    if len(data) != SIZE or hashlib.sha256(data).hexdigest() != DIGEST:
        raise ValueError("Product differs from the recorded snapshot")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Restore missing 16 MB FITS")
    args = parser.parse_args()
    path = ROOT / "data/raw" / FILE
    if args.fetch and not path.exists():
        with urllib.request.urlopen(URL, timeout=90) as response:
            data = response.read(SIZE + 1)
        check(data)
        with path.open("xb") as out:
            out.write(data)
    check(path.read_bytes())
    with fits.open(path) as hd:
        hd.verify("exception")
        primary = hd[0].header
        sci = hd["SCI"].data
        wht, ctx = hd["WHT"].data, hd["CTX"].data
        wcs = WCS(hd["SCI"].header).celestial
        inputs = hd["HDRTAB"].data
        center = SkyCoord(inputs["RA_TARG"][0]*u.deg, inputs["DEC_TARG"][0]*u.deg)
        # Sample pixel centers on an east-left, north-up tangent field.
        step = 0.025
        offsets = (np.arange(240) - 119.5) * step
        west, north = np.meshgrid(offsets, offsets)
        sky = center.spherical_offsets_by(-west*u.arcsec, north*u.arcsec)
        x, y = wcs.world_to_pixel(sky)
        separation = sky.separation(wcs.pixel_to_world(x, y)).arcsec
        if separation.max() > 1e-5:
            raise ValueError("WCS round trip exceeds tolerance")
        good = np.isfinite(sci) & (wht > 0) & (ctx != 0)
        cut = map_coordinates(np.where(good, sci, np.nan), [y, x], order=1,
                              mode="constant", cval=np.nan)
        limits = np.nanpercentile(cut, [1, 99.9])
        meta = {
            "class": "approximate independent reconstruction / public-data demonstration",
            "data_uri": URI, "url": URL, "size_bytes": SIZE, "sha256": DIGEST,
            "program": primary["PROPOSID"], "target": primary["TARGNAME"],
            "detector": primary["DETECTOR"], "filter": primary["FILTER2"],
            "date_observed": inputs["DATE-OBS"][0], "product_date": primary["DATE"],
            "exptime_s": primary["EXPTIME"], "input_ids": list(inputs["ROOTNAME"]),
            "input_exposures_s": inputs["EXPTIME"].tolist(),
            "cal_ver": list(np.unique(inputs["CAL_VER"])),
            "input_dqicorr": list(np.unique(inputs["DQICORR"])),
            "input_sdqflags": np.unique(inputs["SDQFLAGS"]).tolist(),
            "drizcorr": primary["DRIZCORR"], "drizzle_kernel": primary["D001KERN"],
            "pixfrac": primary["D001PIXF"], "units": hd["SCI"].header["BUNIT"],
            "shape_yx": sci.shape, "wcs": list(wcs.wcs.ctype),
            "native_pixel_arcsec": [scale.to_value(u.arcsec) for scale in wcs.proj_plane_pixel_scales()],
            "target_center_deg": [center.ra.deg, center.dec.deg],
            "extensions": [h.name for h in hd], "has_fits_checksums": ["CHECKSUM" in h.header for h in hd],
            "valid_fraction_full": good.mean(), "valid_fraction_cut": np.isfinite(cut).mean(),
            "max_round_trip_arcsec": separation.max(), "display_limits_electrons_per_s": limits.tolist(),
        }
    fig, ax = plt.subplots(figsize=(6.6, 5.6), layout="constrained")
    image = ax.imshow(cut, origin="lower", extent=(-3, 3, -3, 3), cmap="gray",
                      interpolation="nearest", norm=AsinhNorm(linear_width=1., vmin=limits[0], vmax=limits[1]))
    ax.set(xlabel="West of target (arcsec)", ylabel="North of target (arcsec)",
           title="M31 nucleus  ·  HST ACS/HRC F435W")
    fig.suptitle("Public-data demonstration", fontsize=12)
    fig.colorbar(image, ax=ax, shrink=.78, label="Count rate (electrons/s)")
    fig.savefig(ROOT / "figures/hst_f435w.png", dpi=180)
    (ROOT / "docs/hst_product.json").write_text(json.dumps(meta, indent=2)+"\n")


if __name__ == "__main__":
    main()
