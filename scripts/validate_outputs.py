#!/usr/bin/env python3
"""Read-only validation of common ISCE2/MintPy output checkpoints."""
from __future__ import annotations
import argparse, glob
from pathlib import Path
try:
 import h5py
except Exception: h5py=None

def check(ok,label): print(("PASS" if ok else "FAIL")+" "+label); return ok

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("project",type=Path); a=ap.parse_args(); p=a.project.resolve(); ok=True
 patterns=["merged/interferograms/*/filt_fine.unw","merged/interferograms/*/filt_fine.cor","merged/interferograms/*/filt_fine.unw.conncomp"]
 counts=[]
 for pat in patterns:
  n=len(glob.glob(str(p/pat))); counts.append(n); ok &= check(n>0, f"{pat}: {n}")
 ok &= check(len(set(counts))==1 and counts[0]>0,"interferogram product counts agree")
 for rel in ["inputs/ifgramStack.h5","inputs/geometryRadar.h5"]:
  f=p/rel; good=f.exists() and f.stat().st_size>0; ok &= check(good,rel)
  if good and h5py:
   try:
    with h5py.File(f,"r") as h: print("INFO",rel,"datasets",list(h.keys())[:12])
   except Exception as e: ok &= check(False,f"open {rel}: {e}")
 for rel in ["velocity.h5","timeseries_demErr.h5","temporalCoherence.h5"]:
  f=p/rel; check(f.exists(),rel)
 ok &= check((p/"geo").exists(),"geo directory")
 raise SystemExit(0 if ok else 2)
if __name__=="__main__": main()
