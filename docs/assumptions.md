# Assumption and discrepancy ledger

2026-11-23. These are audit findings and decisions to resolve before fitting. No unverified correction has been applied to the original handoff, papers, or public code.

| ID | Evidence / ambiguity | Consequence and next action |
|---|---|---|
| A01 | L18 p.1 and Fig.1 print distance 785 **pc**; their angular/physical scales imply kpc. PT03 p.4 explicitly adopts 0.77 Mpc and 3.73 pc/arcsec; public model code also uses 3.73. | Treat printed 785 pc as an apparent unit typo, not an adopted physical distance. Choose and record the replication scale; ask whether 3.73 was used throughout final analysis. 785 kpc gives about 3.806 pc/arcsec. |
| A02 | L18 §3.6 calls MC uncertainty the standard error of the mean; public `ppxf_m31.py:958-966` uses `np.std` across trials. | With 100 independent draws these differ by a factor of 10. Recover final errors/code path before choosing; do not silently divide by sqrt(N). |
| A03 | L18 §5.1 divides by 1746-4; public `model_fit.py:1194-1200` uses `numgood-5`. | Small numerical normalization discrepancy, but important provenance. Confirm final settings and per-bin versus per-spaxel weighting. |
| A04 | Paper describes +/-15-degree coarse angle grid; theta_a best fit -15 is outside that range about -34.5. Fig.20 visibly spans wider ranges; public code contains coarse/fine and single-point overrides. | Obtain actual grid arrays/run manifest. The current function ends with `Agrid=np.arange(-15)`, an empty array, not [-15]. Never run it blindly. |
| A05 | Public model uses stochastic Gaussian position perturbations; paper objective scatter is dominated by model realizations. | Record RNG algorithm/seed/particle count; compare stochastic convergence with deterministic PSF integration only as a labeled alternative. |
| A06 | Spatially binned data are represented on spaxel maps; §5.1 quotes spaxel count and no full covariance treatment. | Recover actual objective convention. Do not count repeated bin values as independent measurements in a new statistical interpretation. Reproduce original weighting separately from covariance-aware alternatives. |
| A07 | Bulge normalization radius: §3.3 text 10 arcsec, Fig.4 caption 15 arcsec. | Need exact profile normalization or original bulge map; important near edges and for inclination. |
| A08 | Model source normalizes total flux before applying radial mask and uses a wavelength median; paper speaks of flux normalization/collapsed cube more generally. | Recover final image construction, error propagation and normalization domain; test these explicitly. |
| A09 | PSF estimated relative to NIRC2; paper final 124 +/-6 mas and abstract rounded 0.12 arcsec; original code reads `params.txt`. | Use actual kernel/units. Do not treat quoted FWHM as Gaussian sigma or add widths linearly. |
| A10 | PT03 sky axes X west,Y north,Z toward observer; v_LOS=-vZ; OSIRIS display additionally rotated. | Unit-test handedness, rotation order, sky PA, systemic offset and sign with known cases. |
| A11 | PT03 particles fixed; L18 adds rigid precession without self-consistent gravitational response. | For implementation, delta-v = Omega_p*(-y,x,0), with pc and km/s/pc. This is a kinematic prescription, not a self-gravitating evolution. |
| A12 | L18 TW raw result -18 +/-5; calibrated 62 +/-5 in §5.3, 63.0 +/-5.3 in Appendix C. | Record both, ask for final diagnostic settings. Neither is the headline 0.0 +/-3.9 fit. |
| A13 | Table 5 total is weighted and rescaled; profile curves hold other parameters fixed. | Do not interpret 3.4 as standard reduced chi-square or intervals as marginalized credible regions. Test frequentist coverage separately. |
| A14 | KOA broad query gives 12/18/22/23 matching science candidates versus Table 1 13/18/22/23. Narrow queries inconsistently omit nights. | Exact accepted-frame manifest needed; archive absence not established. Inspect original headers/acquisition metadata before selecting, particularly 2008 coordinate offsets. |
| A15 | Paper uses a private-communication, background-subtracted/subsampled F435W product and Lauer98 optical image. | Public current drizzles are candidates for a demonstration, not verified identical historical inputs. |
| A16 | Public source has several dated product families and no publication release marker established. | Ask for final code revision and authoritative products; code inspection alone cannot settle all paper inconsistencies. |
| A17 | C07 threshold depends on stellar disk thickness/mass; h/r=0.4 can require slower precession than the headline 3-10 range. | A low fitted speed is compatibility evidence, not a direct demonstration of gas delivery or star formation. |
| A18 | Gaussian-fit/Gauss-Hermite V and sigma need not equal raw LOSVD moments. | Match the fitted estimator, velocity histogram limits, weighting and normalization; raw moments are only test diagnostics. |
| A19 | Source snapshots lack detected redistribution licenses; pPXF/VorBin declare specific proprietary licenses. | Inspect terms before reuse/distribution. Source evidence is kept locally and Git-ignored. This does not block independent implementation of published mathematics. |

All future resolutions should append the source, date, human input, and downstream outputs affected; preserve the earlier ambiguity as provenance.

## Stage 1 choices · 2026-11-23

A05, A09, A10, A11 and A18 were exercised on synthetic data using deterministic Gaussian PSF mixing, receding-positive velocities and raw LOSVD moments. A15 was exercised with a current ACS F435W association. The toy distributions, masks, objective, geometry and noise assumptions, as well as the observed-image processing choices, are recorded in the [Stage 1 report](stage1.md). The historical settings still require confirmation.

## Independent PT03/STIS checkpoint · 2026-11-23

The red-STIS comparison uses PT03’s own physical scale and Table 1 parameters, a centered PA 39° slit, approximate along-slit edges and the published Eq. 21 PSF. We measured the effects of whole-orbit rejection versus conditional eccentricity redraw, opposite half-pixel slit offsets and a single-pixel extraction. Absolute registration to the historic slit remains uncertain. FQ and FCQ are compared to separate model-side LOSVD fits. [Assumptions and numerical effects](pt03_stis.md)
