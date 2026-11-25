# Historical red STIS aperture audit

2026-11-25. The archive confirms the commanded slit geometry and detector sampling for Bender et al.'s M31 calcium-triplet observations. The P3-relative slit registration and custom extraction boundaries remain unresolved. Recomputing the fixed disk model with the archive position angle has a negligible effect on the approaching-side discrepancy.

## What the archive establishes

- Nine M31 program 8018 G750M products from visits 01 and 02 total **20,790 s**, exactly matching Bender et al. Table 1. All use aperture 52X0.1 and central wavelength 8561 Å. Modulo 180°, the header position angles span 38.97634° to 38.97655°. The commanded across-slit offset is zero in all nine. Along-slit commands range from 0 to 1.443″, with confirmation from the proposal and aperture coordinates. These coordinates follow the nominal pointing line through the proposal target to within a few microarcseconds in the header arithmetic. That arithmetic does not measure actual pointing accuracy on the sky. [Program 8018 proposal](https://www.stsci.edu/hst/phase2-public/8018.pro) · [Header excerpts and file hashes](stis_archive_headers.json)
- A rectified first-exposure product, `o58501020_sx2.fits`, has a spatial axis of 0.050809″ per row. The archived `sx1` files have one extracted spectrum per product. The first uses a seven-pixel extraction. Its extraction keywords describe the pipeline product. The paper's 25 Fourier quotient and 22 Fourier correlation quotient measurements use a separate reduction. The archive products inspected contain no mapping from their rows to those published bins. [Rectified spectrum](https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:HST/product/o58501020_sx2.fits) · [STIS extraction documentation](https://hst-docs.stsci.edu/stisdhb/chapter-5-stis-data-analysis/5-5-working-with-extracted-spectra)
- Bender et al. registered the slit by comparing STIS profiles with WFPC2 brightness cuts. Their reported 0.005″ precision for the red slit pertains to that measurement. The aperture coordinates and commanded dithers do not supply its numerical offset from P3. Bender's tables report radii relative to P3 and give bin centers. Brown & Magorrian also used approximate apertures in their subsequent comparison and explicitly identified the variations in spatial binning as a possible refinement. [Bender et al. §2, Fig. 1 and Appendix](https://chandra.as.utexas.edu/m31stis.pdf) · [Brown & Magorrian §2](https://academic.oup.com/mnras/article/431/1/80/1040222)

## Rerun of the fixed model

All cases use the same one million particles and the session's prior model parameters. The archive-angle case uses 38.97643° and retains the previous midpoint boundaries and centered slit. The other cases use that angle with either an aperture translation of half a rectified row along the slit, or one rectified row centered on each reported radius. The shifts gauge sensitivity to an assumed origin error, not a measurement of the actual registration error.

| Aperture assumption | Velocity at −0.180″ | Velocity at −0.080″ | Inner FCQ velocity RMS |
|---|---:|---:|---:|
| Published nominal angle, baseline | −396.3 | −313.0 | 63.0 |
| Archive position angle | −396.3 | −312.9 | 62.9 |
| Archive PA, apertures shifted northeast by 0.0254″ | −393.7 | −265.8 | 56.2 |
| Archive PA, apertures shifted southwest by 0.0254″ | −394.8 | −355.0 | 74.1 |
| Archive PA, 0.050809″ aperture at each center | −396.6 | −312.9 | 63.6 |
| Observed FCQ | −313.6 ± 14.4 | −181.4 ± 16.1 | |

All velocities are in km/s. The RMS covers the 18 tabulated FCQ centers within 1″. Changing the angle alone moves the inner velocities by at most 0.04 km/s to the precision shown. Along-slit registration can substantially affect the steep inner gradient, but the offset at −0.180″ stays between 80 and 83 km/s in magnitude in these trials. The one-row case is a sensitivity test for unresolved bin widths. Exact historical aperture shapes remain unknown. [Full predictions](pt03_stis_profiles.csv)

## Provenance and remaining inputs

Codex inspected the nine pipeline extractions, the first exposure's rectified spectrum, cosmic-ray-rejected image and support product, and the public observing proposal. The payloads are local under `tmp/stis8018`. The tracked JSON lists their URLs and hashes. Run `.venv/bin/python scripts/stis_archive_headers.py tmp/stis8018` to regenerate the manifest from those products and `.venv/bin/python scripts/pt03_stis.py` to rerun the comparison. Nine tests passed. The model run took about 11 seconds after imports.

The missing historical inputs are the authors' registered red coadd or equivalent STIS-to-WFPC2 transform and the row ranges or weights used in each FQ and FCQ bin. An independently measured slit registration would use the reference WFPC2 imaging and the red STIS light profiles, with the blue nucleus independently located in ultraviolet imaging. That would constrain slit placement. Recovering the exact extraction weights still requires reduction records or a reproducible copy of the historical extraction.
