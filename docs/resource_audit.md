# Resource audit and search record

2026-11-23. This is a bounded public-resource audit, not proof that unlocated material is unavailable anywhere. No credentials were supplied, no author was contacted, and no science FITS file was downloaded. Raw responses are under `docs/evidence/`; their acquisition parameters and checksums are in `acquisition_manifest.json`.

## Papers and supplements

Downloaded and reviewed the full text of L18 (UCL published version), PT03 (arXiv v1), and C07 (arXiv v2), including appendices. Downloaded Bender 2005 and inspected the comparison-data appendix. UCL and [UC eScholarship](https://escholarship.org/uc/item/2190n293) expose article records/PDFs; no intermediate data bundle was located there. The publisher DOI was attempted through web access and direct retrieval: the latter returned a browser challenge page, saved as `publisher.html`. Therefore publisher supplements are **not fully audited**, not established absent. No data/code deposit link was found in the inspected L18 PDF.

Searches included the paper title/DOI/arXiv ID with data/code/supplement terms; Lockhart/M31/GitHub; Peiris/Tremaine/particles/download; the exact filename `nonaligned_model.dat`; and Lockhart/M31/Zenodo. Broad indexed search was noisy and did not locate the input products. Direct inspection of the public JLU repository was substantially more productive. KOA's contributed-data listing was inspected; it did not identify a matching Lockhart release. These negative findings apply only to the searched surfaces and date.

## Public M31 analysis source: located

Repository: [jluastro/JLU-python-code](https://github.com/jluastro/JLU-python-code).
Pinned inspected tree: `22b2cb0d7484ec36713af4e34983b5ccc284d8be` (complete recursive response, `truncated=false`). Local copies of `model_fit.py`, `ppxf_m31.py`, and `paper_2017.py` match the Git blob SHA-1 values in that tree, as well as the SHA-256 hashes in our manifest. Latest returned change to `model_fit.py`: `644e56bad1bbfb7d5aa9b29beab57508a92b4e27` (2017-10-11); preceding history explicitly mentions pre-submission changes. This supports relevance but does not establish the final publication revision.

The tree also contains `bulgesub_m31.py`, `molecfit_m31.py`, `voronoi_m31.py`, `mask_m31.py`, `vlsrcorr_m31.py`, `ifu.py`, `hst.py`, and other M31 helpers. Only the three saved scripts were inspected in detail; the rest are located, not validated.

Important file references in the inspected source:

| Reference | Role | Evidence |
|---|---|---|
| `nonaligned_model.dat` | Six-column disk-plane PT03 particles (pc, km/s) | `model_fit.py` lines 69-71 |
| `params.txt` | Single-Gaussian PSF parameters | `model_fit.py` lines 156-164 |
| `voronoi_2d_binning_output_20160825.txt` | Shared data/model spatial bins | `model_fit.py` line 195 |
| `m31_all_scalederr_cleanhdr_bulgesub_vorcube_20160825` | Model-fitting cube family | `model_fit.py` line 36 |
| `ppxf_tess_bs_2_20160825.dat` | Kinematic fit output | `model_fit.py` line 397 |
| `mosaic_all_nirc2_cc_dtotoff_no100828_scalederr.fits` | Later combined cube without excluded night | `paper_2017.py` lines 10-11 |
| `ppxf_renormlosvd_c11m_bs_tess_sn40.dat` | Later bulge-subtracted, S/N=40 kinematic maps | `paper_2017.py` line 14 |
| `ppxf_errors_mc_nsim100_c11m.dat` | Later kinematic uncertainties | `paper_2017.py` line 17 |

These paths refer to the authors' local machines; their existence in source does not make the files public. The inspected complete repository tree does not contain these exact input products. The code imports local `gcwork`/`jlu` modules and contains legacy IDL and Python pPXF paths. Current grid settings include successive overrides ending in an empty `np.arange(-15)` angle grid. Do not execute the snapshot as a turnkey pipeline. We have not changed or run it.

GitHub reports no detected license for this repository; the tree search found no license-named file. Treat the source as inspectable evidence, with reuse/redistribution terms unresolved. Snapshots are Git-ignored, not vendored as our implementation.

## Keck OSIRIS: candidates located, completeness unresolved

Used documented [KOA TAP access](https://koa.ipac.caltech.edu/UserGuide/PyKOA/TAPClients.html), table `koa_osiris`. Date searches deliberately precede target-name filtering because M31 is sometimes labeled `tt000`/`tt001`. The broad saved query covers `OS.201008%` and `OS.2008102%` and returned 3722 metadata rows. Candidate selection requires the four paper dates, Kbb, scale 0.05 arcsec, 900 s, and the M31-associated target labels. This gives:

| UT date | Paper Table 1 | Archive candidates | PI metadata | Use in paper |
|---|---:|---:|---|---|
| 2008-10-21 | 13 | 12 | M.Rich | Included |
| 2010-08-15 | 18 | 18 | J.Lu | Included |
| 2010-08-28 | 22 | 22 | Ghez | Excluded for image quality |
| 2010-08-29 | 23 | 23 | Ghez | Included |

Total candidates: 75; retained-night candidates: 53, versus 76/54 in the paper. Candidate counts are not a certified accepted-frame list. The 2008 coordinates are offset from the nucleus despite the `M31-nuc` label; pointing/WCS metadata must be reconciled using headers and acquisition history before selection. For 2010 the corresponding science positions cluster around the nucleus. A nearby-coordinate-only selection also picks up acquisitions/guide targets and can give the wrong count.

**Query inconsistency:** the initial four-date OR query returned 142 rows and omitted Aug 29; a repeated OR query with explicit MAXREC returned 99 rows, omitting both late-August nights; a single Aug 29 prefix query returned zero. Yet the broader prefix response contains explicit Aug 29 KOAIDs and file paths, including `OS.20100829.32850.fits`. All responses are preserved. The cause has not been determined. KOA's landing page displayed a maintenance notice, but we cannot attribute this behavior to maintenance without evidence. Do not interpret a zero-row response as proof of absent data. Re-query using an independent access route before bulk acquisition.

The night metadata includes HD209932/HD218633 standards, sky observations, and some darks. This is partial calibration evidence; correct historical rectification matrices, wavelength/flat/bad-pixel products and association completeness are not verified. `filesize_mb` is blank in retrieved OSIRIS metadata. A 2048x2048 32-bit image is about 16.8 MB before FITS overhead, giving roughly 0.9 GB for 53 single-image frames; this is only a planning lower bound, not a measured download size. Multiple extensions, calibration files and derived cubes increase it.

KOA documents its quick-look products as guides to data content rather than science-analysis replacements. They are not the paper's bespoke reduced mosaic. No frame payload was downloaded to test retrieval or scientific usability.

## NIRC2: matching supporting observations

`koa_nirc2.csv` contains 1342 metadata records from the three requested nights. Candidate nuclear observations include eight 30 s narrow-camera Kp frames on 2005-07-29, fifteen 120 s J and fourteen 60 s H narrow-camera frames on 2009-09-10, matching §2.1.2. There are three candidate 5 s wide-camera Kp frames on 2007-10-19; the paper used one. Its exact selection is unresolved. Other filters/exposures were returned too; they are not automatically part of this analysis. Payloads, final combined images, distortion solution and source-registration catalog have not been obtained.

## HST: public products and observation identifiers

MAST queries completed with explicit paging totals. A program-10571 query returned 13 observation records; a 0.005-degree cone around (10.6845833,41.2691667) returned 693 HST records. These queries include multiple product levels, so records must not be summed indiscriminately.

- ACS/HRC program **10571**, 2006-06-15/16: F435W associations `j9am01010` and `j9am01020`, each 1192 s; F330W associations `j9am01030`, `j9am01050`, `j9am01070`, with 2688,2716,2716 s. Totals are **2384 and 8120 s**, matching L18. They are marked PUBLIC. Product metadata lists `_drz.fits` association files of 16,030,080 bytes each. The later combined HAP products are also visible, but are not identical to the historical custom reduction by Lauer.
- WFPC2/PC program **5464**, 1994-10-02: `u2e201...` exposures in F555W/F814W/F1042M and combined products are PUBLIC. Verify the historical processing and exact selected exposures before claiming image replication.
- STIS program **8018**, July 23-24, 1999: G750M records including `o58501020` and `o58502020` are PUBLIC. Bender 2005 explicitly identifies visits 1 and 2 of this program. Its Tables 4-5 provide published stellar kinematics; retrieving current calibrated spectra does not recreate that extraction automatically.

The seven-observation ACS product query returned 620 rows, including duplicate file references through associations. Deduplicate by `dataURI` before estimating a download. The metadata, not FITS contents, were inspected. An example 16 MB image would be a suitable next public-data demonstration; full astrometric/PSF verification belongs to that task.

## Software and external dependencies

| Resource | Verified state | Implication |
|---|---|---|
| [OsirisDRP](https://github.com/Keck-DataReductionPipelines/OsirisDRP) | Public repository; README requires IDL, CFITSIO/build tools and Java GUI; notes Apple M1 workaround. Tags returned v4.0.0 through v6.0.2 but not v3.2. | Historical v3.2 may exist in commit history, but exact revision/calibration compatibility is unverified. No installation attempted. GitHub did not detect a license. |
| [pPXF](https://pypi.org/project/ppxf/) | PyPI snapshot 9.5.2, Other/Proprietary License metadata | Current version is not the paper version; inspect detailed terms and pin a validated version only when needed. |
| [VorBin](https://pypi.org/project/vorbin/) | 3.2.1; official deprecation notice in favor of PowerBin | Exact replication should preserve original bins or algorithm; changing to PowerBin is a methodological change. |
| [Gemini spectral library](https://www2.gemini.edu/observing/resources/near-ir-resources/spectroscopy) | Official indexed description allows downloading late-type templates; live page returned 403 | Library located, exact 23 filenames and payload availability not verified. |
| molecfit / solar spectrum | Required by L18 §3.1; no exact historical inputs/configuration located | Not replaceable by a generic telluric division without documenting a deviation. |

No new dependencies were installed. Existing tools: Python, Poppler, macOS arm64. Version details are in `environment.json`. The current Python ecosystem is appropriate for a small prototype; raw OSIRIS reduction has additional historical and potentially licensed-runtime requirements.
