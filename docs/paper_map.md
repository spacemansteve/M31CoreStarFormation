# Publication and input map

Reviewed 2026-11-23. Page numbers below refer to the local PDFs, not browser line numbers. L18 = Lockhart et al. published version, 23 pages; PT03 = arXiv astro-ph/0307412v1, 45 pages; C07 = arXiv 0704.3831v2, 10 pages. Sources, versions, sizes, retrieval times, and SHA-256 hashes are in `acquisition_manifest.json`. Text was extracted with `pdftotext -layout`; key tables, equations, maps and grid panels were also visually inspected. PDF extraction alone is unreliable for signs, Greek characters, and two-column reading order.

## Lockhart et al. (2018)

| Location | Result or diagnostic | Inputs and transformations | Replication requirement |
|---|---|---|---|
| pp. 1-3; Fig. 1; Table 1 | Nuclear components and observing setup | OSIRIS Kbb, 0.05 arcsec sampling, 900 s exposures, PA 56 degrees; HST/NIRC2 images | Observing and accepted-frame manifest; nuclear component labels are interpretation |
| pp. 3-5; Figs. 2-3; §§3.1-3.2 | Mosaic, S/N, exposure map, PSF | DRP v3.2; dark/bad-pixel/sky/wavelength/cube corrections; standard stars plus molecfit; cross-correlation to NIRC2; clipped combination | Raw/calibration frames and exact recipe, or final and three subset cubes; final PSF fit |
| pp. 4-6; Figs. 4-6; §3.3 | Bulge-light fraction and subtracted spectra | Courteau model M profile scaled to NIRC2 wide image; bulge templates from ratio >=0.42 spaxels; Gaussian LOSVD (-340,110) km/s | Profile normalization, templates and bulge cube; 10 vs 15 arcsec normalization discrepancy needs clarification |
| pp. 6-7, 11-12; Table 2; Figs. 7,15-17 | UV-to-IR registration, P3 morphology, cuts | ACS F330W/F435W, WFPC2 F555W/F814W/F1042M, NIRC2 J/H/K'; successive translation/scale/rotation; source 11 as SMBH | Common-source coordinates, transformation chain, custom background-subtracted/subsampled F435W; 0.033 arcsec total alignment error |
| p. 7; Fig. 8; §3.5 | Voronoi binning | Continuum 2.270-2.280 microns; target S/N 40; discard initial S/N<2; sum spectra and quadrature errors | Exact bin map and footprint; bins must be shared with forward model |
| pp. 7-9; Figs. 9-11; §3.6 | Spectral fits and errors | 23 GNIRS templates with blue/red coverage; fit 2.185-2.381 microns; fourth-order Gauss-Hermite LOSVD and additive degree-4 continuum; 100 MC samples and template jackknife | Template names/resolution matching, pPXF version/settings and errors; SEM/SD ambiguity in ledger |
| pp. 8-10; Figs. 12-14; §4.1 | Velocity/dispersion/h3/h4 maps and extrema | Bulge-subtracted binned spectra fitted by pPXF; systemic correction; peak location relative to SMBH | Authentic map arrays; figure color ranges clip extremes, so digitization cannot recover the maxima reliably |
| pp. 9-13; Table 3; Figs. 18-19; §4.3 | STIS and OASIS comparisons | PA 39-degree STIS cut and PA 56.4-degree OASIS cut; PSF matching and registration offsets | External tabulated kinematics plus OSIRIS maps; Bender 2005 Tables 4-5 are an available independent comparison source |
| pp. 11-15; Tables 4-5; Figs. 20-21; §5.1 | Four-parameter fit and uncertainty curves | PT03 nonaligned particles, rotations, rigid precession, stochastic PSF, shared bins, 5 km/s LOSVD histogram, GH fits; weighted objective | Particles + data/errors/bins/PSF + exact grid and normalization; do not replace GH-fit V/sigma with raw sample mean/std |
| pp. 13-18; Figs. 22-24; §§5.2-5.3 | Model/data residuals for flux, velocity, dispersion | Original PT03 orientation versus fitted orientation; restrict quantitative comparison to inner 1.3 arcsec | Same forward model as fit; plotting normalization differs from total-flux normalization used in fitting |
| pp. 14-16,18; Table 6; Fig. 25; §6 | Literature comparison and gas-feeding interpretation | Published precession estimates and inclination conventions; Chang theory | Literature values are heterogeneous model-dependent estimates, not interchangeable measurements |
| pp. 19-20; Figs. 26-29; Appendix A | Bulge-systematics experiment | Same binning, before/after subtraction; intrinsic templates and h3 correlations | Unsubtracted maps/cube as well as final products; inclination shifts 44 to 29 degrees in the extreme no-subtraction test |
| pp. 20-21; Fig. 30; Appendix B | Registration sources | Eight images with alignment sources marked | Machine-readable source coordinates not supplied by the figure |
| pp. 21-22; Fig. 31; Appendix C | Alternative TW precession residuals | Five strips; model-based calibration for thick disk | Secondary diagnostic, not the main fit; §5.3 and Appendix C give slightly different calibrated numbers |
| pp. 22-23; Fig. 32; Appendix D | PT03 model versus original optical image | Lauer 1998 deconvolved F555W, 0.0228 arcsec pixels; PT03 orientation | Exact historical image and particle distribution; a current archive drizzle is not automatically this input |

### Verified numerical anchors (reference values, not fitted here)

| Quantity | Published value | Location |
|---|---|---|
| Final mosaic spatial resolution | 124 +/- 6 mas | §3.2, p. 4 |
| Dispersion maximum | 381 +/- 55 km/s | Abstract; §4.1 p. 8 |
| Dispersion-peak offset | 0.13 +/- 0.03 arcsec | Abstract; §4.1 gives (+0.09,-0.10) arcsec |
| Orientation (theta_l,theta_i,theta_a) | (-33 +/- 4,44 +/- 2,-15 +/- 15) degrees | Table 4, p. 13 |
| Pattern speed | 0.0 +/- 3.9 km/s/pc | Table 4; §5.3 |
| Fixed BH mass | 1.02e8 solar masses | §5.1 p. 11; PT03 Table 1 |
| Best-fit reduced components F,V,sigma | 99.7,14.1,3.3 | Table 5, p. 15 |
| Individual minima F,V,sigma | 95.6,11.3,3.1 | Table 5 |
| Weighted total: PT03 / TW / best fit | 4.7 / 18.9 / 3.4 | Table 5; Appendix A gives 3.37 for best fit |

The objective in §5.1 is Q = sum_m [chi2_m/(1746-4)] w_m, with m = flux, V, sigma and w_m the inverse minimum reduced chi2 for that moment over the grid. Thus Q is a sum of rescaled components, **not** an ordinary reduced chi-square whose expectation is one. h3 and h4 are excluded. Rounded Table 5 entries give Q approximately 3.355, consistent with the tabulated 3.4; that arithmetic is not independent inference.

The paper uses 100 data perturbations and 100 model-PSF realizations. Its objective-scatter thresholds are 0.01 and 0.08, combined to approximately 0.08. Figure 21 holds the other three parameters fixed; it is not a marginalized posterior. Calibrating coverage independently is a separate future test.

## PT03: the actual model family

Read §§1-5 and figure/table captions. Equations (3)-(6), pp. 9-10, specify right-handed rotations and Kepler orbits. Sky X points west, Y north, Z toward observer; receding-positive v_LOS = -v_Z. Disk-to-sky rotation is Rz(theta_l) Rx(theta_i) Rz(theta_a). Orbital-to-disk rotation is Rz(Omega) Rx(I) Rz(omega).

The DF is not a generic aligned set of equal-eccentricity ellipses. Equations (10)-(17), pp. 11-14, define eccentricity-vector dispersion, radius-dependent inclination dispersion, and a central-hole/outer-cutoff semimajor-axis distribution. Section 3.1 samples a with density proportional to a Sigma(a), eccentricity-vector components from Gaussians, inclinations with sin(I) weighting, and mean anomaly/node uniformly. Reject unbound eccentricities. Table 1 (p. 22) supplies the nonaligned parameters: alpha 0.197, ae 4.45 pc, ag 1.71 pc, w 1.52 pc, a0 1.37 pc, c1 4/pc, c2 4.24 pc, sigma_e 0.307, aI 31.5 pc, sigma_I0 24.6 degrees, and BH mass 1.02e8 solar masses.

Sections 3.2-3.4 describe the **original PT03 fit**, using Lauer photometry and KB99 spectroscopy. Its weighting and optical PSFs must not be mistaken for Lockhart's OSIRIS fit. Figures 2-8 test photometry and ground-based kinematics; Figures 11-15 test STIS predictions; §4.2/Fig.16 discuss thickness; §5 lists missing self-gravity, DF flexibility, bulge mismatch and stellar shot noise. An independent draw from the published DF is possible, but will not recover the exact realization or demonstrate the original observations were replicated.

## Chang et al.: physical interpretation, separate from the stellar fit

Read §§1-4 and Appendix A. Section 2/Figs.1-6 study closed gas orbits in a BH plus eccentric stellar-disk potential, using a softened disk gravity and prescribed pattern speed. This is different physics from simply adding Omega cross r to PT03 stellar velocities. The often-quoted 3-10 km/s/pc threshold depends on disk thickness and adopted masses; §2 notes a lower threshold near 2 km/s/pc for h/r=0.4. Do not treat 10 as a universal cutoff.

Section 3/Fig.7 combines stellar mass loss, cooling and gravitational instability to estimate accumulation and fragmentation; §4 offers gas and stellar-population predictions. The approximately 500 Myr recurrence is a model estimate. Appendix A uses PT03 mean eccentricity/effective density profiles and an 8 pc semimajor-axis cutoff; that cutoff must not silently be imposed on a PT03 particle reconstruction without checking its provenance.

The retrieved C07 PDF prints an August 2021 draft-typesetting date but carries arXiv v2 dated June 21, 2007. Record the arXiv version and file checksum; do not interpret the typesetting date as a new scientific revision.

## Additional literature staged

Bender et al. (2005), [author-hosted PDF](https://chandra.as.utexas.edu/m31stis.pdf), is downloaded; its Appendix, Tables 4-5 and program 8018 statement were inspected for comparison-data availability. The entire paper has not been critically reviewed. Brown & Magorrian (2013), [article](https://doi.org/10.1093/mnras/stt104), provides an alternative orbit-superposition approach; record as context, not a substitute PT03 implementation. Tremaine (1995), TW84, Sambhus & Sridhar (2000), and later gas/precession literature remain the next contextual reading queue, after the core replication inputs are settled.
