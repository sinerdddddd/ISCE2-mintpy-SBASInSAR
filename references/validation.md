# Validation checklist

## Environment

- `import isce` succeeds and reports the expected version.
- `smallbaselineApp.py -v`, `stackSentinel.py -h`, `looks.py -h`, `gdalinfo --version` succeed.
- Executables resolve from the intended environment, not system Python.

## ISCE2

- Number of generated `configs/config_generate_igram_*` files agrees with planned pairs.
- `run_files/` exists and every submitted run has a success marker in its log.
- `merged/interferograms/*/filt_fine.unw`, `.cor`, and `.unw.conncomp` counts agree.
- `merged/geom_reference` contains the files required by the MintPy template.

## MintPy HDF5

Open files with h5py and check dataset names, shape, dates, wavelength, finite values, and expected `ALOOKS`/`RLOOKS`. Counts must match the planned interferogram/date inventory.

## ERA5

Check that every time-series date has corresponding meteorological coverage, the requested UTC hour is consistent, GRIB/HDF5 files are non-empty, and the corrected output can be opened before replacing or archiving the uncorrected product.

## GeoTIFF/export

Use `gdalinfo` to check raster size, nodata, pixel size, geotransform, and CRS when the source is geocoded. Count files against dates/pairs; verify `pairs.csv` paths; create and test a checksum manifest after archiving.
