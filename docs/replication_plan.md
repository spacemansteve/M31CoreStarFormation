# Staged replication plan

2026-11-23. Stage 0 is reported in the decision memo. The subsequent [Stage 1 report](stage1.md) records completion of the small numerical prototype and one public imaging demonstration. The [independent PT03/STIS comparison](pt03_stis.md) now tests a new draw from the published distribution against the public red-slit measurements. The authentic OSIRIS-input stage remains pending.

## Small numerical verification prototype

Implement a small Python package with an isolated environment, explicit units, and an executable example. Start with approximately 10,000 synthetic particles and small maps; increase only after timing and convergence checks. Do not install OSIRIS reduction dependencies at this point.

1. Implement Kepler coordinates/velocities and the two rotations from PT03 Eqs.3-6, with named coordinate frames and receding-positive LOS velocities. Verify circular limits, periapse/apoapse speeds, Kepler residuals, energy/angular momentum conservation, and rotation inverse/determinant/norm checks.
2. Add the rigid-precession prescription, delta-v=Omega cross r, before sky projection. Verify all four quadrants, axes, origin, zero speed and reversed sign. The Kepler invariants apply before this imposed velocity term, not to the modified velocities as though they were unperturbed orbits.
3. Construct explicitly synthetic observations from known inputs. Verify PSF flux conservation on a padded domain and flux-weighted LOSVD mixing before fitting moments. Convolving V or sigma images directly is not generally equivalent to convolving the spectra/LOSVDs.
4. Demonstrate recovery of zero and nonzero injected precession on a small grid. Include positive and negative injections, noise, varying bin size, and multiple seeds. Include a face-on degeneracy case rather than promising recovery where the data contain no information. Document finite-particle bias and test tolerances before interpreting fit differences.
5. Keep the toy model and any later PT03 DF sampler distinct. A faithful independent PT03 sampler follows its published density and rejection rules, including sin(I) weighting; it is an independent realization, not the original file.

**Gate:** all mathematical checks pass, recovery limitations are explained, and a short timing/memory estimate is reported before expanding the grid. Every figure must say SYNTHETIC TEST. No observed Lockhart target values may be used to tune this toy recovery.

## Separate public-data demonstration

Use one or two public ACS/HRC program-10571 products, after selecting exact dataURI and deduplicating the product list. Association drizzles are about 16 MB each. Check FITS headers, units, WCS, calibration version, detector geometry, data-quality mask and exposure time; record hashes. Produce a small correctly oriented nuclear image, optionally a UV/blue comparison with consistent PSF and registration. Label it **approximate independent reconstruction / public-data demonstration**, not a reproduction of the private Lauer background-subtracted image or the OSIRIS kinematic fit. This can proceed independently of Kelly's files after the Stage 0 report.

## Authentic-input replication

First obtain the minimal bundle in the decision memo. Validate array shapes, units, masks, bin indices, SMBH position, velocity frame, PSF and errors. Record source rights and immutable hashes. Do not deserialize untrusted pickle files; prefer documented numeric formats or an audited conversion of trusted author products.

Reproduce observable maps and extrema before parameter fitting: figures 8,10,12-14; then model comparisons 22-24, and finally grid/objective curves 20-21 and Tables 4-5. Compare with preregistered metrics: pixel/bin residuals, flux normalization, peak values/positions, component objectives and parameter intervals. Establish tolerances from precision, interpolation, pixelization and stochastic convergence, not by tuning until published numbers appear.

Recover the authors' exact grid, normalization, degrees of freedom, weights and uncertainty calculation. Resolve or explicitly branch the paper/code discrepancies in `assumptions.md`. Preserve the original statistical procedure for replication; perform covariance-aware likelihoods or alternative uncertainty procedures as separately labeled sensitivity studies.

**Gate:** authentic inputs and usable run configuration are present; miniature forward-model tests pass; estimated full-run resources are reported. Ten million particles require at least 480 MB for six float64 arrays alone, with multiple intermediate arrays potentially using several GB. The nominal paper coarse grid has 7^3*13=4459 cells, but the actual grid is unresolved. Benchmark one model and a small subset before allocating a full search. No full-grid runtime is currently measured.

If the original particles cannot be obtained, a new draw from the PT03 DF may support an **approximate independent reconstruction**, with convergence and distribution checks. If observations remain unlocated, the result remains a synthetic implementation test regardless of agreement with tabulated targets.

## Raw-frame route: only after a separate feasibility review

Reconcile KOA responses and the missing 2008 candidate; obtain accepted/rejected frame IDs. Identify sky/standards/darks/rectification matrices and historically appropriate DRP v3.2 code/calibrations. Verify the IDL/build environment on this arm64 host, preferably with an isolated reproducible environment, before bulk transfer. Determine actual file sizes and total disk requirements.

Reduce one representative science frame plus calibration subset. Validate wavelength solution, spectral resolution, bad-pixel/sky behavior, spatial orientation and telluric correction against the paper before mosaicking. Recover NIRC2 registration, empirical error scaling from three subset cubes, bulge subtraction, and template selection. The raw route is conditional, not scheduled or authorized as a large download by this staging task.

## Later interpretation and extensions

After evaluating replication, test PSF, alignment, bulge profile, templates, fixed BH mass, thickness and stochasticity. Keep self-consistent stellar dynamics, gas-flow simulations, alternate orbit libraries, and later gas constraints separate from the original reproduction. Report what additional empirical evidence would distinguish models.

Each stage adds a work-log entry with inputs, AI action, human intervention, verification, outcome, compute and limitations. Preserve failures and inaccessible resources as results of the AI capability experiment.
