# Stage 0 decision memo

2026-11-23. Scope: literature and resource audit; no re-reduction, parameter inference, or author contact.

## Decision

Proceed next with a bounded synthetic implementation-verification prototype and pursue the authentic intermediate products in parallel. Do not begin a full raw-frame reduction or claim numerical replication of Lockhart's fit. A modest public HST imaging demonstration is also feasible, but must be reported separately from the OSIRIS replication.

## What can be reproduced now?

| Level | Current feasibility | Missing prerequisite |
|---|---|---|
| A: paper tables/figures from released products | Published numerical tables can be transcribed and their arithmetic checked. Public HST images support an independent imaging demonstration. Exact OSIRIS maps and residual figures are not yet reproducible. | Final maps/cube, masks, bin definitions, error arrays, registration, and model maps/particles |
| B: inference from observations plus PT03 | Public modeling code and the mathematical model are available for inspection. Authentic-input inference remains blocked. | Original particle realization plus matching data products; publication-era settings/commit |
| C: raw-frame reduction through inference | Relevant OSIRIS and NIRC2 metadata and HST products are located. Completeness and historical calibration/reduction compatibility are not established. | Accepted exposure list, rectification/calibration products, pipeline v3.2 configuration, telluric recipes, IDL/runtime feasibility, all Level B inputs or an explicitly independent PT03 reconstruction |

The strongest new resource is [the public M31 module in JLU-python-code](https://github.com/jluastro/JLU-python-code/tree/22b2cb0d7484ec36713af4e34983b5ccc284d8be/jlu/m31). It contains reduction, kinematics, modeling, and paper-figure routines. The inspected model file's history includes a 2017 pre-submission update. This is strong evidence of relevance, **not confirmation that the current files reproduce the final published analysis**.

## What would help from Kelly?

The highest-value request is a small intermediate-product bundle, not all raw observations:

1. Final flux, velocity, dispersion, h3/h4 maps and errors; spatial-bin membership; footprint/fit masks; pixel scale, position angle, SMBH coordinates, velocity zero point, and units. FITS or documented numeric arrays would be ideal.
2. The exact PT03 `nonaligned_model.dat` used for fitting, with provenance, units, particle count, any weights, and permission for reuse. The public reader expects six columns: x, y, z, vx, vy, vz.
3. The final PSF parameter file (`params.txt` is referenced), fit grid/objective settings, and the code revision/run command used for the publication. Please clarify MC standard deviation versus standard error, four versus five fitted degrees of freedom, and the adopted angular-to-physical scale.
4. If maps are unavailable: final combined and three subset cubes, their uncertainty arrays, and the bulge-subtraction/telluric configuration. Public scripts refer to both 2016 and later `ppxf_renormlosvd...` product families; which family is authoritative?
5. For a later raw reduction: the accepted exposure manifest, especially the 2008 October 21 count, calibration/rectification matrices and DRP settings; the custom Lauer F435W product and registration-source coordinates.

Exact example filenames and code locations are in [the resource audit](resource_audit.md). No messages have been sent. Nothing is needed from the user to continue a synthetic prototype; Kelly's products would unlock genuine inference much sooner.

## What would success demonstrate?

A successful authentic-input replication would show that we can recover the published observables and the reported fit under the same assumptions, with documented numerical tolerances and discrepancies. It would not independently prove the disk's true precession is zero, establish a self-consistent stellar dynamical equilibrium, or prove that stellar winds formed P3. The adopted stellar model omits disk self-gravity and adds precession kinematically. Chang et al.'s gas-inflow argument includes additional physical assumptions and thickness-dependent limits.

For the AI experiment, success includes a reproducible account of which steps needed human explanations, unavailable products, historical software, or scientific decisions. The audit has already exposed a practical distinction: published methods and public code can be inspectable while the exact numerical experiment remains unrecoverable without its intermediate files.
