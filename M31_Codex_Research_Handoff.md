# Codex Research Handoff: Reproducing Lockhart et al. (2018) on the M31 Nuclear Stellar Disk

**Prepared:** 2026-11-23  
**Project:** AI and the Future of Astronomy Research — empirical reproduction experiment  
**Status:** Starting brief, not a claim that the original data or model code have been obtained.

## 1. Your assignment

You are Codex operating locally on the user's Mac. Investigate and, as far as the available public materials permit, reproduce the measurements and dynamical modeling in:

**K. E. Lockhart, J. R. Lu, H. V. Peiris, R. M. Rich, A. Bouchez, and A. M. Ghez (2018), “A Slowly Precessing Disk in the Nucleus of M31 as the Feeding Mechanism for a Central Starburst,” The Astrophysical Journal 854, 121 (23 pp).**

- DOI: https://doi.org/10.3847/1538-4357/aaaa71
- arXiv: https://arxiv.org/abs/1710.01394
- Published version PDF: https://discovery.ucl.ac.uk/id/eprint/10044861/1/Lockhart_Slowly_Precessing_Disk_VoR.pdf
- Institutional landing page: https://discovery.ucl.ac.uk/id/eprint/10044861/
- ADS search: https://ui.adsabs.harvard.edu/search/q=doi%3A10.3847%2F1538-4357%2Faaaa71

**Primary goal:** quantify which portions of a real astronomical research workflow can be performed *independently and verifiably* by a frontier coding/AI agent and which require missing resources, expert scientific judgment, observational constraints, or physical model choices.

**Secondary goal:** construct a reproducible research package with figures, tests, provenance and an explicit separation between original findings, replicated results, approximations and new hypotheses.

This is **not** initially a mandate to make a new discovery, and is **not** permission to describe simulated or digitized measurements as original observations.

## 2. Scientific background

The nucleus of M31 (Andromeda) contains a supermassive black hole orbited by an eccentric disk of **old stars**, associated with the nuclear light concentrations P1 and P2; a compact, **young** stellar component (P3) occupies the central region. A scientific question is how gas reached the central region and fueled the young population despite the extreme tidal environment. One hypothesis (Chang et al. 2007) is that mass lost from old stars collides, shocks, and flows inward when the eccentric disk precesses slowly enough.

Lockhart et al. obtained high-resolution adaptive-optics, near-infrared integral-field spectroscopy from **OSIRIS on Keck II**, mapped the old disk's line-of-sight stellar kinematics, and compared the observations with **Peiris & Tremaine (2003)** eccentric disk models. This is a mix of observational reduction, statistical inference, orbit/dynamical modeling, and theoretical astrophysical interpretation—not a formal mathematical proof.

Important paper facts to check against the PDF:

- AO-assisted OSIRIS spatial resolution approximately **0.12 arcseconds FWHM** (~0.45 pc at M31).
- Nuclear old stellar disk region approximately **r < 4 pc**.
- Peak measured velocity dispersion **381 ± 55 km/s**, displaced **0.13 ± 0.03 arcseconds** from the SMBH.
- Fitted orientation **(theta_l, theta_i, theta_a) = (-33 ± 4, 44 ± 2, -15 ± 15) degrees**.
- Fitted precession **Omega_P = 0.0 ± 3.9 km/s/pc**, i.e. consistent with no measured precession, **not** proof of exact zero.
- Adopted Peiris & Tremaine nonaligned model black hole mass **1.02 × 10^8 solar masses**.
- Their model starts from roughly **10^7 particles** in disk-plane coordinates; these are rotated into candidate orientations, a solid-body precession term is added, projected onto the line of sight, PSF-smoothed, and compared with observed flux/velocity/dispersion maps.
- The fitting uses a grid over **theta_l, theta_i, theta_a, Omega_P**, and a combined weighted goodness-of-fit measure. See §5, Tables 4–5, Figures 20–24.
- Explicit limitation: this is **not** a self-consistent simulation including disk self-gravity and self-consistent precession (§6). A good fit demonstrates compatibility within model assumptions; it does not prove the gas-feeding hypothesis.

Useful conceptual distinction: *verifying an implementation* (algorithmic/mathematical checks) versus *validating an astrophysical model* (agreement with independent observations and physical realism).

## 3. Paper roadmap — read this before coding

Consult the actual published PDF rather than relying on abstracts or this brief.

- §2 / Table 1: observing runs, OSIRIS setup, NIRC2/HST imaging, acquisition details. Keck/OSIRIS runs listed: **2008 Oct 21; 2010 Aug 15; 2010 Aug 28–29**; paper excludes the Aug 28 night because of poor spatial resolution.
- §3: OSIRIS data reduction, telluric correction, bulge subtraction, registration, spatial binning, stellar spectra extraction and kinematic estimation. Figure 8 documents Voronoi spatial bins; pPXF / template mismatch analyses matter.
- §4: observed flux and 2D kinematic maps; comparisons with HST/STIS and CFHT/OASIS.
- §5.1: model transformations, projection, Gaussian positional perturbations approximating PSF, velocity distribution, fitting grid, Monte Carlo error estimate.
- §5.2–5.3 / Table 4: orientation and precession estimation. **Do not confuse the main model result with the alternative Tremaine–Weinberg calculation**; the paper reports why the latter performs poorly for the thick disk.
- §6: physical meaning and limitations, especially lack of self-gravity, uncertainty of precession and the indirect nature of the starburst mechanism inference.
- Appendices: instrumental/spectral/registration checks and alternative precession comparisons.

## 4. Preliminary numerical targets (comparison anchors, not hard-coded answers)

| Quantity | Paper value | Where to verify |
|---|---|---|
| theta_l | -33 ± 4 degrees | Abstract, Table 4, §5.2 |
| theta_i | 44 ± 2 degrees | Abstract, Table 4, §5.2 |
| theta_a | -15 ± 15 degrees | Abstract, Table 4, §5.2 |
| Omega_P | 0.0 ± 3.9 km/s/pc | Abstract, Table 4, §5.3 |
| SMBH mass, assumed | 1.02e8 solar masses | §5.1 |
| Observed dispersion maximum | 381 ± 55 km/s | Abstract, §4 |
| Peak dispersion offset from SMBH | 0.13 ± 0.03 arcsec | Abstract |
| Best-fit weighted total in Table 5 | about 3.4 | Table 5; verify exact definition |

**Do not assume these parameters can be reproduced without original processed observations and PT03 particle realization.**

## 5. Important prior work and resources

### Direct methodological antecedents

1. **Peiris & Tremaine (2003)**, dynamical model of the eccentric nuclear stellar disk of M31, the basis for Lockhart et al.'s fits. Locate through paper bibliography/ADS; determine whether actual model particle realizations and code are public. Their model should not be silently replaced by a generic Keplerian disk.
2. **Chang et al. (2007), “The Origin of the Young Stars in the Nucleus of M31.”** https://arxiv.org/abs/0704.3831 — physical hypothesis connecting stellar-wind gas inflow, slow disk precession and the young nuclear cluster.
3. **Tremaine (1995), “An Eccentric Disk Model for the Nucleus of M31.”** https://arxiv.org/abs/astro-ph/9502065 — conceptual basis for eccentric nuclear disk.
4. **Brown & Magorrian (2013), “Three-dimensional Keplerian orbit-superposition models of the nucleus of M31.”** https://doi.org/10.1093/mnras/stt104 — alternative modeling approach, NOT interchangeable with PT03.
5. **Tremaine & Weinberg (1984)** and **Sambhus & Sridhar (2000)** — precession estimation method mentioned in §5.3. Understand the thin-disk assumption and why the paper's alternative result is inconsistent with the principal fit.

### Software / data portals to assess (availability unverified)

- Keck OSIRIS data reduction pipeline cited by the paper: https://github.com/Keck-DataReductionPipelines/OsirisDRP
- Keck Observatory Archive (KOA): https://koa.ipac.caltech.edu/ — search the target, dates, instrument, PI and data-access status. Check rights and calibration frames, not just science FITS files.
- HST MAST archive: https://mast.stsci.edu/ — relevant HST imaging and STIS comparisons, if useful and available.
- NASA ADS: https://ui.adsabs.harvard.edu/ — literature and citation graph; use APIs only within documented quotas/credentials.
- Python/Astropy ecosystem: https://www.astropy.org/ ; FITS via astropy.io.fits, WCS, units, tables, modeling.
- pPXF (Cappellari): https://pypi.org/project/ppxf/ — LOSVD / stellar kinematics, check license and version provenance.
- Voronoi spatial binning (Cappellari & Copin 2003): identify a maintained implementation and cite version.

The existence of portals/software does **not** establish that Lockhart's exact raw frames, reduced data cubes, binned LOSVD maps, and PT03 model particles are publicly obtainable. Treat availability as the first research question.

### Later literature — context, not replication targets

- 2024 paper on counter-rotation/recoil kicks and slow eccentric-disk precession: https://arxiv.org/abs/2408.13353 . Useful eventually to distinguish what was concluded in 2018 from subsequent hypotheses.
- Newer gas constraints in the M31 nucleus: https://doi.org/10.1051/0004-6361/202347597 . Keep separate from first-pass reproduction.

## 6. Execute in stages; stop at meaningful checkpoints

### Stage 0 — Literature and resource audit (FIRST)

1. Download **and read** the full Lockhart PDF, its appendices, and PT03 and Chang et al.; record local paths, versions and retrieval dates.
2. Build `docs/paper_map.md` mapping each important figure/table/claim to input dataset(s), transformations, estimated parameters and code needed.
3. Search literature, publisher supplementary materials, authors' public repositories, KOA/MAST, and institutional repositories for **machine-readable intermediate products and model particle distributions**. Verify rather than guess.
4. Create `docs/data_inventory.csv` with: item, role, source URL/identifier, access status, size, license/rights, checksum if downloaded, reduction level, and reproducibility implications.
5. Produce a feasibility assessment of *three levels*: (A) paper-table/figure reproduction from released products; (B) parameter inference from data + PT03 models; (C) full raw-frame re-reduction and inference. Choose the simplest scientifically legitimate entry point.
6. Clearly list unlocated datasets, private codes, calibration dependencies, and **specific questions that Kelly Lockhart or the authors could answer**. Do not presume access or contact them automatically.

**Checkpoint:** Do not undertake a large raw-data download or extensive simulation until Stage 0 is reported. If core data are inaccessible, propose a faithful synthetic-data unit-test and a separate public-data demonstration, each prominently labeled.

### Stage 1 — Methodological reconstruction and verification tests

- Document coordinate conventions, angular and physical scales, projection, line-of-sight velocity convention, PSF model, observational masks, spectral templates, continuum handling, kinematic moments, noise/errors, binning, parameter ranges and goodness-of-fit weights.
- Derive and independently test the orbital mechanics/coordinate transformations. Use dimensionally checked units and toy systems whose answers are known.
- Implement a minimal **toy eccentric-disk model** solely as an *implementation test*, with generated synthetic observations and known injected orientations/precession. It is **not** equivalent to reimplementing PT03 or reproducing Lockhart's physical fit.
- Tests: conservation/invariance where applicable, zero-pattern-speed recovery, injected-pattern-speed recovery, orientation/rotation convention checks, PSF convolution, reproducibility across random seeds, sensitivity to noise and binning.
- Record all choices and unresolved ambiguities in an assumption ledger; cite source pages/sections.

### Stage 2 — Scientific replication using authentic inputs (only if available)

- Start with the most advanced openly accessible *real* data product (e.g., reduced cube or published kinematic maps). Reproduce figures and intermediate metrics **before** fitting parameters.
- If raw OSIRIS frames and calibrations are available, attempt pipeline reduction only after assessing compatibility with original instrument modes, historical reductions, tellurics, sky/background subtraction, distortion, AO PSF and calibration files.
- If actual PT03 particles are available, use those; otherwise explicitly distinguish an alternative independent model from a paper reproduction.
- Fit flux, velocity and velocity-dispersion maps with the paper's grid or a demonstrably equivalent objective. Preserve the original treatment of spatial covariance, uncertainties, weights and central masks where recoverable.
- Run a parameter-recovery injection suite and MC uncertainty tests. Compare numbers and figure shapes with the paper; quantify tolerances and discrepancies, rather than tweaking settings until answers match.
- Classify all outputs: **exact reproduction / approximate independent reconstruction / synthetic test / unable to reproduce**.

### Stage 3 — Critical interpretation and possible extensions (separate, optional)

- Test sensitivity to assumptions: point-spread function, astrometric registration, bulge subtraction, stellar templates, fixed SMBH mass, particle noise, disk thickness, and likelihood weighting.
- Explore alternative models only after original replication is evaluated; don't conflate a new result with a replication.
- Evaluate what would need *new empirical evidence* to distinguish models or support the stellar-wind inflow hypothesis.
- Read the more recent literature for context and possible falsifying constraints.

## 7. Research automation / AI capability log (essential to the larger project)

For every meaningful task, log:

| Field | Record |
|---|---|
| Task and scientific objective | What is being tested? |
| Input provenance | Paper section, dataset URL, software version |
| AI action | What Codex proposed/wrote/ran without a human-provided solution |
| Human input | Domain explanation, scientific decision, credentials, intervention |
| Verification | Automated tests, independent calculation, empirical comparison |
| Outcome | Pass/fail/partial/inconclusive, quantitative discrepancy |
| Blocker | Data access, ambiguity, computing, instrumentation, conceptual modeling |
| Confidence/limitations | What is and isn't supported |

We aim to distinguish: **formal/algorithmic correctness**, **numerical reproducibility**, **statistical fitting**, **empirical model validity**, and **original scientific reasoning**. Track the time, compute resources and human interventions where reasonably possible.

## 8. Local engineering guidelines

- Default stack: Python, an isolated `venv` or `uv` environment, NumPy/SciPy, Astropy, matplotlib, pytest; add pPXF and astronomy-specific packages only as needed.
- Favor Apple Silicon-compatible packages if on Apple Silicon; inspect the actual Mac architecture first. Avoid assuming GPU/CUDA is available.
- Use versioned source, `README.md`, `pyproject.toml`, tests, notebooks for exploration, command-line scripts for reproducible pipelines.
- Separate `data/raw/`, `data/interim/`, `data/processed/`, `models/`, `src/`, `tests/`, `figures/`, `docs/`. Do not commit large datasets or secrets; provide acquisition scripts and checksums/manifest.
- Preserve original science products read-only; track coordinate frames, units, FITS headers, instrument metadata, and exact cuts/masks.
- Fix random seeds, record package versions, CPU architecture and provenance; log all expensive runs and commands.
- Avoid gratuitous compute or downloads; first estimate size, runtime and disk footprint. Request human approval for unusually large workloads, data purchases, privileged access or author contact.
- Do not fabricate unavailable data or claim to have reproduced a published result merely by plotting values copied from its tables.
- Document any deviation from the paper and why it was necessary.

## 9. Initial deliverables requested from Codex

**First session: Stage 0 only** (unless all materials already happen to be present and the next stage is clearly low-cost):

1. `README.md`: science goal, scope, reproducibility status and quick-start.
2. `docs/paper_map.md`: an annotated reading map of the publication, especially §3, §5, relevant tables/figures.
3. `docs/data_inventory.csv`: verified available/unavailable inputs and provenance.
4. `docs/replication_plan.md`: staged minimum viable replication, clearly marked prerequisites and gates.
5. `docs/ai_work_log.md`: the beginning of an evidence-based AI autonomy/verification ledger.
6. A short decision memo: **What can be reproduced now? What requires Kelly's help? What would a successful replication demonstrate?**

**After presenting these, proceed to a small, tested numerical/geometry prototype.** Prefer a functioning verified miniature over a sprawling unvalidated research codebase.

## 10. Questions worth asking Kelly later (not prerequisites to start)

- Are reduced OSIRIS cubes, extracted flux/velocity/dispersion maps, bin definitions and uncertainties archived or shareable?
- Are the precise Peiris–Tremaine particle realizations or model-generation scripts still available?
- Which modeling/reduction steps were the most difficult or dependent on tacit instrumental expertise?
- What is the minimal trustworthy subset of the paper to reproduce independently?
- Which model assumptions or sources of systematic error would she revisit with today's tools?
- Would she consider the gas-inflow/starburst interpretation well supported, merely consistent, or still speculative?

## 11. Suggested first message to Codex

> Read `M31_Codex_Research_Handoff.md` in full. Start with Stage 0. Obtain and inspect the primary Lockhart et al. (2018) PDF and the Peiris & Tremaine (2003) model paper. Audit source data and model availability, map figures to inputs, and produce the requested first-session files. Do not assume the original reduced observations or PT03 particle data are public. Do not start expensive computation or bulk downloads yet. Tell me explicitly what you were able to verify and what you couldn't.

---

**Provenance note:** This brief was assembled from the published Lockhart et al. article as retrieved via a public indexed PDF rendering and corroborating publication records. The full PDF has **not** been locally downloaded and independently parsed in this handoff-creation session. Codex must read the actual PDF (including figures, tables and appendices) as its first step and correct this brief where necessary.
