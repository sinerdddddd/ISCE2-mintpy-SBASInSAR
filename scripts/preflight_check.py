#!/usr/bin/env python3
"""Read-only preflight checks for an ISCE2/MintPy project."""
from __future__ import annotations
import argparse, importlib.util, shutil
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    args=ap.parse_args(); p=args.project.resolve()
    checks=[]
    checks.append((p.exists(), f"project_root: {p}"))
    for name in ["SLC","orbits","DEM","AUX","workdir"]:
        checks.append(((p/name).exists(), f"directory: {name}"))
    for exe in ["stackSentinel.py","smallbaselineApp.py","load_data.py","gdalinfo"]:
        checks.append((shutil.which(exe) is not None, f"executable: {exe}"))
    for mod in ["isce","mintpy","h5py","osgeo"]:
        checks.append((importlib.util.find_spec(mod) is not None, f"python module: {mod}"))
    for ok,label in checks: print(("PASS" if ok else "FAIL")+" "+label)
    raise SystemExit(0 if all(x[0] for x in checks) else 2)
if __name__ == "__main__": main()
