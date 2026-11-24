# Stage 1 results · 2026-11-23

The miniature orbit model recovered its injected speed and orientation on a noiseless grid. With noise, freeing all three angles moved one angle by 10° and the speed by 4 km/s/pc in the joint test. These experiments verify the implementation and expose a limitation of the velocity-only objective. The observational output is a separate image of M31's nucleus.

## Synthetic disk and measurement

The black hole is the origin. PT03 equations 5–6 give the bound Kepler position and velocity for semimajor axis, eccentricity and mean anomaly. We solve Kepler's equation by bisection. Both transformations use the active rotation Rz(node) Rx(inclination) Rz(apsis), first from each orbit into the disk and then from disk to sky. We add Ω(−y, x, 0) in disk coordinates before the second rotation. Sky X increases west and Y increases north. Receding velocity equals −VZ. Positions use pc, velocities km/s, and Ω uses km/s/pc. [Peiris & Tremaine, §2](https://arxiv.org/abs/astro-ph/0307412)

Each synthetic observation uses 10,000 equal-light particles. Semimajor axes are uniform from 0.5 to 3 pc, eccentricities uniform from 0.15 to 0.50, and mean anomalies and nodes uniform in phase. Tilts follow a Rayleigh distribution with 5° scale, and the sum of the node and periapse angles follows a normal distribution with 12° scatter around zero. The adopted GM is 430,000 pc (km/s)². These choices define an arbitrary thick eccentric disk. The PT03 distribution function and the original particle realization remain separate replication inputs.

Particles deposit light on an 88 × 88 grid with 0.125 pc pixels. A circular Gaussian PSF with 0.15 pc standard deviation acts on the light, light times velocity, and light times squared velocity. We sum the blurred planes into square bins before dividing by light. This computes the raw mean and dispersion of a spatially mixed line-of-sight velocity distribution. There are no angular distance conversions, mock spectra, stellar templates, continuum fits, bulge subtraction, or Gauss–Hermite estimates in this experiment.

## What the checks established

Five unit tests cover the Kepler residual, orbital energy and angular momentum up to eccentricity 0.99, circular and apsidal speeds, rotation handedness/order, and the sign of the velocity seen by an observer. They also cover rigid motion in all four quadrants, on the axes and at the origin. An explicit two-channel velocity distribution independently checks PSF mixing, including a particle near the padding boundary. Total light agrees to floating-point precision. The noiseless recovery checks use a separate scalar expansion for sky projection, while injection and fitting share the orbit sampler and spatial measurement code.

We injected −12, 0 and +12 km/s/pc at angles (24°, 55°, −20°) and searched −24 through +24 in steps of 2 km/s/pc. The fixed-orientation objective is the sum of squared mean-velocity residuals divided by (8 km/s)², using bins containing at least 12 particle-equivalents in both maps. The predicted mean is linear in Ω for fixed positions, so two computed maps determine the entire speed grid. Noise was added independently per bin after PSF mixing. Each seed and bin size uses the same noise across injected speeds and model sizes to make paired comparisons.

| Model and fit | Tests | Result |
|---|---:|---|
| Shared draw, orientation fixed, noiseless | 3 seeds × 2 bin widths × 3 speeds | 18/18 exact grid recoveries |
| Shared draw, orientation fixed, noisy | 18 | 18/18 exact |
| Independent 10,000-particle model, noisy | 18 | 12 exact, 6 low by one grid step |
| Independent 40,000-particle model, noisy | 18 | 15 exact, 3 low by one grid step |
| Face-on disk | 25 candidate speeds | Objective identical at every speed, including with the disk's internal thickness |

The coarse bins are 0.50 pc and the fine bins are 0.25 pc. Each independent model is compared to the same 10,000-particle observation. The overlap mask can change with the model draw. Three paired seeds and two model sizes give a sensitivity check. Establishing convergence, systematic bias or statistical coverage would require additional independent trials. [Per-trial results](synthetic_recovery.csv)

For a separate joint test, we varied each of the three angles over three values and the speed over 25 values, using 25 common bright bins with observed light above 150 particle-equivalents. The noiseless minimum recovered (24°, 55°, −20°, +12) with a squared residual score below 10⁻²⁵. With one 8 km/s noise draw, the minimum was (24°, 55°, −10°, +16), with score 16.30 versus 16.53 at the injected parameters. The two fits are close enough that this noisy realization cannot distinguish the injected apsidal orientation and speed reliably. Lockhart's fit also used flux and dispersion and a different objective. The synthetic run gives no estimate of M31's pattern speed. [Synthetic maps](../figures/synthetic_disk.png)

The suite took 1.49 s after imports and peaked at about 108 MiB of process memory on the arm64 Mac, including plotting, the larger comparison models and grid evaluation. The linearity shortcut applies to the raw mean at fixed geometry. These timings do not predict the cost of the authors' LOSVD fitting pipeline.

## Public Hubble imaging demonstration

The F435W association j9am01010 combines four 298 s ACS/HRC exposures from 2006 June 15. We verified the 16,030,080-byte product against its recorded SHA-256 and checked the FITS structure. CALACS 10.4.1 and completed input data-quality initialization are recorded in the headers. The drizzle used a square kernel with pixfrac 1. The 1164 × 1137 science array is in electrons/s at 0.025 arcsec/pixel. The association supplies weight and context arrays. Individual input DQ planes and internal FITS checksum cards are absent. [MAST product](https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:HST/product/j9am01010_drz.fits)

We required finite science values, positive weight and at least one contributing exposure indicated by context. This retains 88.13% of the full rectangle. We sampled a 6 × 6 arcsec field by bilinear interpolation around the header target coordinates, with north up and east left. All 240 × 240 display pixels have valid coverage. The maximum WCS round-trip error is below 4 × 10⁻¹⁰ arcsec. This tests coordinate arithmetic; absolute registration to the black hole would require an external reference. The cutout shows two brightness peaks. The origin is the commanded target, and the asinh stretch is for display. We have applied no custom bulge subtraction, component identification or kinematic fit. [Image](../figures/hst_f435w.png) · [Header, mask and hash record](hst_product.json)

## Published STIS comparison data

The red calcium-triplet STIS spectra probe the old P1/P2 population. Tables 4 and 5 of Bender et al. give two reductions of the same observations. We extracted all 25 Fourier quotient (FQ) rows and all 22 Fourier correlation quotient (FCQ) rows with their errors, and checked the column ordering, minus signs and values against rendered pages 297–298. The spatial bins differ between reductions. FQ supplies V and σ, and FCQ additionally supplies h3 and h4. The two reductions should be retained separately. [Published reference measurements](bender_reference.csv) · [Bender et al., §§2–3 and Appendix](https://chandra.as.utexas.edu/m31stis.pdf)

Both reductions put their highest tabulated dispersion at −0.080 arcsec. FQ gives 373 ± 48 km/s there, while FCQ gives 300.7 ± 23.1 km/s. These are the authors' measurements and errors. They demonstrate how much the choice of velocity-profile estimator matters in this bin. Their shared photons preclude treating the two estimates as independent measurements.

The red G750M slit was 0.1 arcsec wide at PA 39° with 0.051 arcsec per detector pixel along the slit. Bender places zero radius at P3 and positive radius toward P1. The CSV preserves Bender's radii and tabulated velocities without applying a systemic-velocity correction or astrometric shift. Lockhart Fig. 18 uses radius increasing southwest, opposite Bender's direction. Reverse the spatial axis when comparing those displays and confirm velocity reference and registration before scoring residuals. The header target of the separate public image does not define this slit origin. Rebuild the table with `python3 scripts/bender_reference.py` after restoring the pinned PDF and installing Poppler. [Lockhart et al., §4.3.1 and Fig. 18](https://doi.org/10.3847/1538-4357/aaaa71)

## Authentic-input checkpoint

The original OSIRIS fit still depends on the final maps and errors, bin membership, registration, PSF and original PT03 particles. On receipt, recover the observed maps and the registered STIS slit comparison before fitting. A fallback that remains possible with public inputs is an independent PT03 distribution-function implementation and a forward model of the STIS slit. That would use a new particle realization and require validation against the published distribution and slit/PSF geometry. [Author-product checklist](decision_memo.md)
