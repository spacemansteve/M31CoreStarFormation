# A fixed PT03 disk through the Hubble slit

**Approximate independent reconstruction · 2026-11-23.** A fresh draw from the published non-aligned Peiris–Tremaine disk predicts the receding rotation peak and the location of the velocity reversal in the old stellar population. On the approaching side the model rotates too fast, and at large radii its velocity dispersion is too low. The model parameters were fixed before comparison with the observations. [Profile figure](../figures/pt03_stis.png) · [All predictions and residuals](pt03_stis_profiles.csv)

## Comparison with observed stars

The primary comparison uses the Fourier correlation quotient (FCQ) measurements from Bender Table 5. The modeled line profiles were fitted with a fourth-order Gauss–Hermite series, following PT03. Radius is measured along PA 39°, with zero at P3 and positive toward P1. Velocities are receding-positive, relative to the galaxy. We retained Bender's velocity zero point and used zero bulk velocity for the model, without fitting a position or velocity shift. [Bender et al., Appendix](https://chandra.as.utexas.edu/m31stis.pdf) · [PT03, §§3.3 and 4.1](https://arxiv.org/abs/astro-ph/0307412)

| Quantity | Independent disk | Hubble FCQ | PT03 non-aligned prediction |
|---|---:|---:|---:|
| Receding peak, km/s (radius) | +203.3 (+0.592″) | +203.6 ± 3.5 (+0.592″) | +198 (+0.61″) |
| Approaching minimum, km/s (radius) | −396.3 (−0.180″) | −316.4 ± 12.7 (−0.254″) | −369 (−0.20″) |
| Velocity reversal, radius | +0.121″ | +0.126″ | +0.12″ |
| Dispersion peak, km/s (radius) | 342.7 (−0.130″) | 300.7 ± 23.1 (−0.080″) | 328 (−0.10″) |

The independent and observed peaks above are extrema over the **same 22 tabulated apertures**. The velocity reversal uses linear interpolation between the two bins bracketing zero. The last column uses PT03 Table 3 model extrema, converted to Bender's opposite radial sign convention. PT03 used a different radial sampling and an earlier version of the STIS data. Comparing amplitudes at a common position further exposes the discrepancy. At −0.180″ the independent disk predicts −396.3 km/s against the observed −313.6 ± 14.4 km/s. At −0.080″ it predicts −313.0 km/s against −181.4 ± 16.1 km/s. On the P1 side the close match at the peak does not extend to every radius or line-shape coefficient.

For the 18 FCQ centers within one arcsecond, unweighted root-mean-square model-minus-data differences are **63.0 km/s** in velocity, **29.5 km/s** in dispersion, **0.078** in h3 and **0.048** in h4. The model captures the sign of the central negative h3 dip and positive h4 feature. For the four FCQ centers beyond one arcsecond its dispersions average 53.4 km/s below the observations. A separate Gaussian LOSVD fit at the 25 Fourier quotient (FQ) apertures gives inner RMS differences of 49.5 and 25.1 km/s in velocity and dispersion (21 centers). The two reductions share spectra. They should not be combined as independent evidence. The reported RMS values describe residuals and do not assign a likelihood to the model.

## How the prediction was made

1. **Orbital distribution.** We used the non-aligned column of PT03 Table 1, with black-hole mass 1.02 × 10⁸ solar masses, distance scale 3.73 pc/arcsec, and disk-to-sky angles (−42.8°, 54.1°, −34.5°). The semimajor-axis density is proportional to a³ exp(−a/1.37) times the Fermi cutoff at 4.24 pc, sampled by gamma proposals and rejection. At each a we draw both eccentricity-vector components around the signed mean from Eq. 12 with component scatter 0.307. The baseline redraws unbound eccentricities at the same a to preserve the radial marginal in §3.1. Rayleigh proposals accepted with probability sin(I)/I give the inclination density in Eq. 18. Node and mean anomaly are independent uniform angles. Each accepted orbit carries equal light. Sky projection uses the existing Kepler implementation and zero pattern speed.
2. **Instrument.** The slit is 0.1″ wide, centered on the adopted black hole. Its positive axis points northeast on the sky. PT03 Eq. 21 specifies the radial intensity of a Gaussian core and a ring term centered at 0.105″. We normalize it in two dimensions and integrate spilled light into rectangular apertures. Across the slit, the Gaussian-plus-ring blur and the slit width are each applied once. The along-slit baseline edges are midpoints of adjacent reported radii, extrapolating half a spacing at each end. These are estimates because the tables give centers. The comparison uses the bulge-subtracted red stellar measurements, so the forward model contains only disk light.
3. **Velocity extraction.** The program accumulates an aperture-weighted distribution of line-of-sight velocities (LOSVD) in 5 km/s channels, then fits the binned distribution by equal-weight least squares with free amplitude. FCQ uses V, σ, h3 and h4 in the van der Marel–Franx convention. FQ uses a Gaussian. These are model-side proxies for the spectral estimators. We have not applied a stellar-template extraction, instrumental line broadening or the observational Wiener filter. PT03 describes a template correction to the observations and omits that filter in its own model comparison. [PT03 Eqs. 3–6, 10–12, 17–19 and 21](https://arxiv.org/abs/astro-ph/0307412) · [Gauss–Hermite convention](https://arxiv.org/abs/1607.08538)

## Numerical and observational sensitivity

Four independent NumPy PCG64 seeds (7101–7104) supplied 250,000 particles each. Each seed used five 50,000-particle chunks. The quoted baseline fits pool their histograms. Effective particle counts, (Σw)²/Σw², exceed 2,960 in every baseline aperture. At most 0.030% of baseline aperture light fell outside the fitted velocity range of approximately ±4,000 km/s. The largest estimated Monte Carlo standard errors across the inner FCQ bins were 3.93 km/s for V and 3.10 km/s for σ, calculated from four separate fits. Doubling from the first half-million to the full million changed either quantity there by at most 5.48 km/s. These diagnostics address particle noise only.

| Change to baseline, evaluated on shared draws | Largest absolute change in inner FCQ V | Largest absolute change in inner FCQ σ |
|---|---:|---:|
| Move slit 0.025″ northwest | 17.1 km/s | 5.0 km/s |
| Move slit 0.025″ southeast | 28.1 km/s | 15.4 km/s |
| Use one 0.051″ pixel centered on each reported radius | 7.4 km/s | 10.5 km/s |
| Discard entire initially unbound orbit, including its semimajor axis | 16.4 km/s | 8.8 km/s |

The discard-orbit branch addresses PT03's wording about rejecting points with e ≥ 1. It drops 30,637 first proposals from the shared sample and changes the radial marginal. The offset tests represent half-pixel sensitivity, not a measurement of the historical pointing error. Even the southeast shift, which brings the velocity at −0.080″ closest to the observation among these cases, predicts −284.9 km/s there. The individual changes tested do not explain the full discrepancy. None was selected to refit the disk.

The CSV retains each scenario and method separately. Columns starting with `delta_` give model minus the [observed value](bender_reference.csv), `mc_se_` gives the estimated full-sample standard error from four seeds, and `half_shift_` gives the full result minus the first two seeds. Light is in particle-equivalents. The GH coefficients and their differences are dimensionless.

## Reproduce and interpret

From the repository root with the [project environment](../README.md) installed:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/pt03_stis.py
```

Nine tests passed, including independent radial and inclination quadrature, the conditional noncentral chi-squared eccentricity law, the PA sign, direct two-dimensional aperture integration, and recovery of known line-profile coefficients. A 0.005″ PSF mesh missed the point-source throughput tolerance of 0.0008 by 0.00000041 at one test point. We refined the mesh to 0.0025″. Across all baseline apertures this refinement changed V by at most 0.12 km/s and σ by at most 0.10 km/s. The five-scenario run took 5.4 seconds after imports and peaked at 212 MiB on the arm64 Mac. All inputs came from the staged papers and observations.

This establishes a quantitative public-data benchmark for the old eccentric stellar disk. It also identifies where our implementation departs from the published model prediction itself. For example, the approaching peak is about 27 km/s faster in magnitude than PT03 Table 3. The highest-value independent follow-up would recover the actual red-slit placement, extraction-bin boundaries and line-profile processing before trying to infer new disk parameters. The original PT03 particle file and Lockhart OSIRIS maps remain important for the separate precession replication.
