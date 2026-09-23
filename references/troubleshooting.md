# Troubleshooting decision guide

| Symptom | First evidence | Safe action |
|---|---|---|
| `FileNotFoundError` for DEM/VRT | `pwd`, `readlink -f`, VRT source path | Fix the link or regenerate the VRT; rerun the affected setup stage |
| command not found | `which`/`Get-Command`, environment activation | Fix PATH and activation in the job script; rerun preflight |
| OOM / memory cgroup | scheduler log and peak memory | Reduce threads, request more memory, or split the stage; preserve completed outputs |
| no bursts to extract | AOI, DEM bounds, SAFE footprint | Check overlap and clip DEM to the actual footprint |
| missing interferogram outputs | failed run log, pair name | Repair and rerun the failed run plus documented dependents |
| MintPy `KeyError` | generated cfg and installed MintPy version | Re-copy the official default template; change only project paths; do not invent obsolete keys |
| CDS HTTP 502/timeout | PyAPS/CDS log and credentials | Retry with bounded attempts; if persistent, switch to the manual CDS route and keep partial downloads |
| TIFF has no CRS | source HDF5 metadata and `gdalinfo` | Treat ML radar TIFFs as non-geocoded unless a transform/CRS is explicitly present; use `geo/*.h5` for GIS products |
