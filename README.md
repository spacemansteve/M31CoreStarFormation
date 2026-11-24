# M31 nuclear disk: reproduction and AI research audit

**Independent STIS comparison · 2026-11-23. A fresh sample of the published PT03 disk predicts the rotation peak on the P1 side and overpredicts rotation on the opposite side. Replication of the Lockhart OSIRIS fit still awaits its inputs.**

The initial commit (`6ae2bd1`) records approximately **15 minutes of Codex work** on the literature and resource audit, using the supplied research handoff. This is the project owner’s estimate of elapsed work time.

We are assessing how independently an AI agent can reproduce the observations and dynamical modeling of Lockhart et al. (2018), *A Slowly Precessing Disk in the Nucleus of M31 as the Feeding Mechanism for a Central Starburst*, [ApJ 854, 121](https://doi.org/10.3847/1538-4357/aaaa71). The scientific target is the old eccentric stellar disk's orientation and precession, using authentic observations and the Peiris & Tremaine (2003; PT03) model.

The literature and resource audit found public analysis code and relevant archive records. It did **not** locate the final OSIRIS science cube/maps, associated bin/error products, or the original PT03 particle file. These are the shortest route to a faithful replication. Raw-frame completeness and historical calibration compatibility remain unresolved.

[PT03/STIS comparison](docs/pt03_stis.md) · [Observed and predicted slit profiles](figures/pt03_stis.png)

[Stage 1 results and limitations](docs/stage1.md) · [Synthetic maps](figures/synthetic_disk.png) · [Public ACS/HRC image](figures/hst_f435w.png)

## Start here

- [Decision memo](docs/decision_memo.md): what is feasible now and what Kelly could supply.
- [Paper map](docs/paper_map.md): figures, tables, methods, inputs, and comparison targets.
- [Data inventory](docs/data_inventory.csv): access evidence, rights, sizes, and missing inputs.
- [Replication plan](docs/replication_plan.md): next steps and scientific gates.
- [Assumption ledger](docs/assumptions.md): paper/code differences that must not be silently resolved.
- [Resource audit](docs/resource_audit.md): archive searches, public code findings, and limits of negative results.
- [AI work log](docs/ai_work_log.md): actions, verification, human input, and blockers.

## Quick start

The Stage 1 prototype was tested on macOS arm64 with Python 3.14.7. From the repository root, reproduce the installed environment and outputs with the following commands. The HST command fetches one 16 MB product if missing and checks its digest before use.

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-stage1.txt -e .
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/synthetic_demo.py
.venv/bin/python scripts/pt03_stis.py
.venv/bin/python scripts/hst_demo.py --fetch
```

The historical Stage 0 checks use the Python standard library.

```bash
python3 scripts/verify_manifest.py
python3 scripts/summarize_archives.py
```

`docs/acquisition_manifest.json` records retrieval sources and hashes for local evidence. To recover missing evidence, inspect the requests first, then run:

```bash
python3 scripts/fetch_sources.py --fetch-missing
```

This fetches only the listed papers, source snapshots, and metadata; it does not download FITS science frames or run the authors' code. Existing files are verified, not overwritten. Archive responses can change, so a changed checksum requires a new documented audit snapshot.

## Layout and provenance

`literature/` contains downloaded PDFs and derived text. `docs/evidence/` contains unmodified archive responses and public source snapshots, for inspection only. Both are excluded from Git; the tracked acquisition manifest allows retrieval and verification. `data/raw/`, `data/interim/`, `data/processed/`, `models/`, `src/`, `tests/`, and `figures/` hold the project inputs, implementation and outputs. Original input products must remain unchanged; write derived outputs to a separate directory.

The original [handoff](M31_Codex_Research_Handoff.md) is preserved. Corrections and uncertainties are recorded in the audit documents. Public visibility is not a software redistribution license; no third-party code is incorporated into our implementation.

Every future scientific output must identify its class: **exact reproduction**, **approximate independent reconstruction**, **synthetic test**, or **unable to reproduce**. A transcription of a published result is reference data, not a recovered measurement. Algorithmic verification, numerical replication, and empirical model validity are separate achievements.

The [published STIS slit measurements](docs/bender_reference.csv) now have a fixed-parameter [model comparison](docs/pt03_stis.md) with explicit registration and sampling sensitivities. The authentic-input request and full-grid prerequisites are in the decision memo.
