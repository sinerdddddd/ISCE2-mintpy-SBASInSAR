---
name: isce2-mintpy-sbas-insar
description: Plan, run, resume, validate, and export Sentinel-1 TOPS SBAS-InSAR projects using ISCE2 topsStack and MintPy, including ERA5 correction and GeoTIFF products.
metadata:
  short-description: ISCE2 + MintPy SBAS-InSAR workflow
---

# ISCE2 + MintPy SBAS-InSAR

Use this skill when the user needs an end-to-end Sentinel-1 TOPS SBAS-InSAR workflow: environment checks, ISCE2 `topsStack`, staged SLURM execution, MintPy loading/inversion, optional ERA5 tropospheric correction, or ML/GIS GeoTIFF export.

Do not assume the example paths, dates, AOI, cluster partition, resource values, software versions, or data counts from the reference manual. First collect or infer a project configuration, then run the preflight checks and present the planned stages.

## Required operating pattern

1. Read [references/workflow.md](references/workflow.md) for the state machine and restart rules.
2. Read [references/parameters.md](references/parameters.md) and resolve project paths, AOI, dates, looks, versions, platform, and SLURM resources.
3. Run `scripts/preflight_check.py` against the project directory before generating or submitting jobs.
4. Execute one stage at a time. After each stage, validate the success criteria in [references/validation.md](references/validation.md); do not submit downstream jobs after a failed checkpoint.
5. For failures, use [references/troubleshooting.md](references/troubleshooting.md) to diagnose and choose the smallest safe restart point.
6. For ERA5, read [references/era5.md](references/era5.md). Never put CDS credentials in scripts, logs, or archives.
7. Before delivery, run `scripts/validate_outputs.py`, record versions and configuration, and report missing checks or assumptions.

## Decision rules

- If the platform is unclear, separate Linux/SLURM commands from Windows commands and ask for the target execution environment before submitting jobs.
- If a required input or credential is missing, stop at preflight and request it; do not invent a path or silently skip the stage.
- Treat large HDF5 files as compute-node work. Do not recommend destructive deletion unless the restart rule explicitly allows it and the user has authorized the run.
- Preserve intermediate products until the corresponding downstream checkpoint passes.
- Use the official MintPy default template as the base and change only project-specific keys; keep a backup of the generated template.

## Deliverables

Report the produced products and QC evidence: ISCE2 run logs, `inputs/ifgramStack.h5`, `inputs/geometryRadar.h5`, MintPy time-series/velocity products, optional ERA5 outputs, ML/GIS GeoTIFF directories, `pairs.csv`, archive files, and checksums. Link to the relevant files when they exist.
