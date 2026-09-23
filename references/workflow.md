# Workflow and restart state machine

`prepare ? stack_configured ? isce_completed ? mintpy_loaded ? inversion_completed ? troposphere_corrected ? exports_verified`

## Stages

- **prepare**: environment, inputs, DEM conversion, orbit/AUX availability, writable project and scratch space.
- **stack_configured**: `stackSentinel.py` completed; `configs/`, `run_files/`, and the network graph exist.
- **isce_completed**: all planned `run_XX` jobs succeeded; expected `merged/interferograms` and `merged/geom_reference` files exist.
- **mintpy_loaded**: `inputs/ifgramStack.h5` and `inputs/geometryRadar.h5` open with h5py; dimensions, dates, wavelength, and looks are consistent.
- **inversion_completed**: velocity, time-series, coherence, and geo products exist and are readable.
- **troposphere_corrected**: only after the ERA5 files and date coverage pass validation; record whether correction was applied or intentionally skipped.
- **exports_verified**: TIFF counts, raster dimensions, nodata, CRS/geotransform where applicable, and archive checksums pass.

## Safe resume rules

- Failed ISCE2 run: repair the cause and rerun that run file or the smallest dependent set. Do not regenerate the whole stack without checking existing outputs.
- Failed `load_data`: remove/rebuild only `inputs/ifgramStack.h5` when the input interferograms are valid; preserve geometry and configs unless validation shows they are wrong.
- Failed `invert_network`: remove only the partial products documented by the current MintPy version (`timeseries.h5`, `temporalCoherence.h5`, `numInvIfgram.h5` as applicable), then resume from `invert_network`.
- Failed export: keep all HDF5 products and rerun only the exporter.
- Never delete source SLC, orbit, DEM, `merged/`, or the only copy of an HDF5 product as a generic cleanup step.
