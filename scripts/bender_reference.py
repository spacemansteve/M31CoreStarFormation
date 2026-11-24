"""Extract two published numerical tables from the pinned Bender et al. PDF."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PDF = "literature/bender2005.pdf"


def main():
    files = json.loads((ROOT / "docs/acquisition_manifest.json").read_text())["files"]
    expected = next(item["sha256"] for item in files if item["path"] == PDF)
    if hashlib.sha256((ROOT / PDF).read_bytes()).hexdigest() != expected:
        raise ValueError("Unexpected Bender PDF revision")
    rows = []
    for page, method, columns, count in [(18, "FQ", 5, 25), (19, "FCQ", 9, 22)]:
        page_text = subprocess.check_output(
            ["pdftotext", "-layout", "-f", str(page), "-l", str(page), ROOT / PDF, "-"],
            text=True)
        # This PDF's embedded font maps the printed minus to U+0001.
        numeric = re.compile(r"^\s*(-?\d+\.\d{3})\s*\.{2,}\s+(.+?)\s*$")
        subset = []
        for line in page_text.replace("\x01", "-").splitlines():
            match = numeric.match(line)
            if match:
                values = [match[1], *match[2].split()]
                if len(values) != columns or not all(re.fullmatch(r"-?\d+(\.\d+)?", v) for v in values):
                    raise ValueError(f"Unexpected table layout on page {page}")
                subset.append(values)
        radii = [float(v[0]) for v in subset]
        if len(subset) != count or sorted(set(radii)) != radii:
            raise ValueError(f"Unexpected rows in {method} table")
        rows.extend([[method, *v, *([""] * (9-columns))] for v in subset])
    with (ROOT / "docs/bender_reference.csv").open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("method", "radius_arcsec", "v_kms", "v_error_kms", "sigma_kms",
                         "sigma_error_kms", "h3", "h3_error", "h4", "h4_error"))
        writer.writerows(rows)


if __name__ == "__main__":
    main()
