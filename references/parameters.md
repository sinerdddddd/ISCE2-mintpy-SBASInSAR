# Project configuration contract

Before execution, resolve these fields. Store the resolved values in a project config or run manifest.

```yaml
project_root: /path/to/project
slc_dir: SLC
orbit_dir: orbits
aux_dir: AUX
dem_file: DEM/dem.wgs84
aoi: {south: 0.0, north: 0.0, west: 0.0, east: 0.0}
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
polarization: VV
orbit_direction: ascending
looks: {azimuth: 6, range: 30}
connection: 2
num_proc: 4
num_proc_topo: 4
platform: linux-slurm
partition: null
software: {python: null, isce2: null, mintpy: null, gdal: null, pyaps3: null}
run_era5: false
export_ml_tiff: false
export_geo_tiff: true
```

Validate `stackSentinel.py -h`, `smallbaselineApp.py -v`, and `gdalinfo --version` in the target environment. Resource estimates in the original manual are examples only; size jobs from actual image count, raster dimensions, and available memory.
