# AI autonomy and verification ledger

## Session 001: Stage 0, 2026-11-23

**Scientific objective:** determine which parts of the Lockhart et al. experiment are reproducible from verifiable public inputs, and stage the next work without substituting synthetic data for observations.

**Human input:** the user supplied `M31_Codex_Research_Handoff.md` and authorized literature search, resource audit, and staging. No scientific solution, credentials, data products, or methodological clarification was provided during this audit. No author contact occurred. One primary agent performed the work; no subagents were used.

| Task | Input provenance | AI action | Verification | Outcome / blocker / limitations |
|---|---|---|---|---|
| Review scope | Original handoff, read in full | Extracted stages, goals and epistemic boundaries | Compared requested deliverables with staged files | Complete; stopped at Stage 0 report rather than starting simulation |
| Acquire literature | UCL L18 VoR; arXiv PT03 v1 and C07 v2 | Downloaded PDFs, extracted text, reviewed main text/appendices and key visuals | Local PDFs readable; SHA-256 recorded; tables/rotations/grid visually checked | Complete for core audit reading; not independent verification of every derivation |
| Map claims to inputs | L18 §§2-7, Appendices A-D; PT03 equations/tables; C07 gas physics | Wrote figure/table map and numerical anchor ledger | Matched Table 4/5 values and method details to PDF; distinguished main fit from TW | Complete; identified distance, grid, error and normalization ambiguities |
| Find author code | JLU-python-code recursive tree and history | Located M31 scripts; inspected three source snapshots without executing them | Computed Git blob hashes match pinned tree; history includes 2017 pre-submission work | Public relevant code found; exact publication revision, inputs and reuse rights unresolved |
| Audit OSIRIS | KOA TAP metadata on four nights plus broad prefixes | Queried instrument/time/target metadata and calibration candidates | Recomputed 12/18/22/23 science-candidate counts from broad response | Partial; one 2008 frame discrepancy, pointing offset, inconsistent narrow queries; no payload usability verified |
| Audit NIRC2 | KOA supporting-night metadata | Filtered camera/filter/time candidates | Counts match eight Kp, fifteen J, fourteen H; three wide Kp candidates for one chosen frame | Partial; exact accepted wide frame and combined images unknown |
| Audit HST | MAST CAOM filtered/cone/products responses | Identified ACS 10571, WFPC2 5464, STIS 8018 | Complete paging; public rights fields; 2384/8120 s ACS totals; deduplicated product identifiers | Public products located; custom historical image reductions not acquired |
| Locate comparison data | Bender 2005 author PDF | Inspected appendix, Tables 4-5 and program identification | Matched program 8018 to archive records | Comparison tables available; not yet transcribed or re-extracted |
| Audit software and supplements | DRP README/tags; PyPI metadata; official library description; publisher/UCL/UC pages | Recorded available software, missing historical configuration and blocked publisher access | Saved API metadata; distinguished challenge page from article; noted current versions differ from historical | Partial; DRP v3.2/calibrations and template subset unresolved; no packages installed |
| Stage reproducible audit | Saved evidence and notes | Wrote manifest, acquisition/verification/count scripts, inventory, plan, assumption ledger and decision memo | SHA-256 and Git blob checks pass; count script reproduces report | 23 acquired evidence files, 27 inventory items; science replication not started |

## Compute, provenance and intervention record

Host: macOS arm64, Python 3.14.7, Poppler 26.08.0; see `environment.json`. No GPU work, numerical model fitting, raw reduction, or new dependency installation. Acquired sources/metadata total **17,189,688 bytes** (about 17.2 MB), excluding derived PDF text/preview images. No FITS science payload was downloaded. Local rendering and metadata parsing are small workloads; no empirical full-model runtime estimate exists yet.

The first primary PDF download completed at 16:24 UTC (11:24 EST). At 16:36 UTC, approximately 12 minutes had elapsed since that download; this is a lower bound on audit wall time, not CPU time or total chat time. Exact per-file completion timestamps are recorded in the manifest. No token-cost or total tool-CPU telemetry is available, so none is estimated.

Initial sandboxed network retrieval failed DNS resolution; authorized public downloads succeeded with network escalation. Initial Git initialization was blocked by filesystem sandbox restrictions and retried with escalation. These are environment interventions, not scientific blockers or user-supplied research solutions. KOA query inconsistencies and publisher/Gemini access failures are preserved as audit limitations rather than silently interpreted as absent resources.

## Verification and scientific status

`python3 scripts/verify_manifest.py`: verifies all 23 acquired files against byte counts/SHA-256, plus the three public-source blobs against the pinned Git tree.

`python3 scripts/summarize_archives.py`: independently recomputes the documented candidate counts, ACS totals and deduplicated association-image sizes from saved responses. This validates audit bookkeeping, not observational reduction or astrophysical inference.

Current classes: literature/source audit **complete within stated scope**; exact reproduction **not attempted / blocked on authentic inputs**; approximate reconstruction **planned**; synthetic test **planned**; gas-feeding hypothesis **not tested**.

Next meaningful log entry should record either receipt of authentic products, resolution of an assumption, or the first verified synthetic prototype. Do not overwrite this session's blockers merely because a later session resolves them.

## Stage 1 · 2026-11-23

The owner selected Astra High, authorized the next steps and described a temporary delay in contacting Kelly. Codex chose the toy distributions, grid, random seeds, PSF and public association and implemented both experiments. No author contact or new science inputs from Kelly were needed. The original 15-minute estimate applies to the initial audit commit.

The executable orbit/PSF checks passed. The independent-draw experiment produced one-grid-step shifts, and the noisy joint fit shifted one angle and the speed. We retained both discrepancies. One 16,030,080-byte public FITS product was downloaded, checked, masked, oriented and rendered. No OSIRIS frames were downloaded. The isolated scientific environment is pinned. A sandboxed timing utility could not query the kernel clock rate, so the final benchmark uses Python wall-time and process RSS. [Results, provenance, compute and remaining inputs](stage1.md)

Codex also extracted all 47 rows of the two published Bender red-STIS reductions from the hash-pinned PDF, inspected rendered journal pages 297–298, and documented the radius convention, slit geometry and peak dispersions. This is a transcription of observed reference data. Independent extraction from the spectra and registration to OSIRIS remain open.

## Independent PT03/STIS comparison · 2026-11-23

The owner requested the next independent step. Codex implemented the published non-aligned distribution, the STIS PSF and slit, and two LOSVD estimators. Four particle draws predicted both tabulated red-STIS reductions. Human input was limited to choosing this direction. No author contact, new downloads, or parameter fitting to the observed stars occurred. The first PSF quadrature check marginally failed its tolerance. Halving the mesh spacing passed with changes below 0.12 km/s in baseline V. Nine tests passed. Registration and radial-bin boundaries are approximations. The red-side rotation peak agrees, while the approaching-side mismatch exceeds draw-to-draw fluctuations. [Numerical results, sensitivities and timing](pt03_stis.md)
