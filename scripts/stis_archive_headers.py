"""Record the provenance and spatial metadata of the program 8018 products."""
import argparse
from hashlib import file_digest
import json
from pathlib import Path

from astropy.io import fits
import numpy as np

PRODUCT_IDS = ("o58501020", "o58501040", "o58501060", "o58501080", "o585010a0",
               "o58502020", "o58502040", "o58502060", "o58502080")


def summarize(path):
    with path.open("rb") as stream:
        sha256 = file_digest(stream, "sha256").hexdigest()
    record = dict(file=path.name, size_bytes=path.stat().st_size, sha256=sha256)
    if path.suffix != ".fits":
        record["url"] = "https://www.stsci.edu/hst/phase2-public/8018.pro"
        return record
    record["url"] = "https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:HST/product/" + path.name
    with fits.open(path) as hdus:
        hdus.verify("exception")
        record["hdus"] = [hdu.name for hdu in hdus]
        keys = ("PROPOSID", "ROOTNAME", "APERTURE", "OPT_ELEM", "CENWAVE", "POSTARG1",
                "POSTARG2", "EXPTIME", "TEXPTIME", "RA_TARG", "DEC_TARG", "RA_APER",
                "DEC_APER", "PA_APER", "PLATESC", "CAL_VER", "CTYPE2", "CRPIX2",
                "CRVAL2", "CD2_2", "SHIFTA2")
        record["header"] = {key: hdus["SCI"].header.get(key, hdus[0].header.get(key))
                            for key in keys if "SCI" in hdus and
                            (key in hdus["SCI"].header or key in hdus[0].header)}
        if path.name.endswith("_sx1.fits"):
            sci = hdus["SCI"]
            sizes = np.unique(sci.data["EXTRSIZE"])
            record.update(spectral_rows=len(sci.data), extraction_heights_pixels=sizes.tolist())
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("download_dir", type=Path)
    args = parser.parse_args()
    files = [f"{root}_sx1.fits" for root in PRODUCT_IDS]
    files += ["8018.pro", "o58501020_sx2.fits", "o58501020_crj.fits", "o58501020_spt.fits"]
    records = [summarize(args.download_dir / name) for name in files]
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
