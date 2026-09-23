# ERA5 / PyAPS3 guidance

Use ERA5 only after the MintPy time series and geometry files validate. Confirm the requested UTC hour, date range, spatial area, pressure levels, and PyAPS3/MintPy compatibility. The original manual uses 11:00 UTC for its example; this is a project choice, not a universal default.

Preferred order:

1. Try PyAPS3 automatic download with bounded retries.
2. If CDS download fails, inspect whether the failure is authentication, rate limiting, network, or a missing request. Do not repeatedly submit identical requests without a stopping condition.
3. Use `cdsapi` only with credentials already configured outside the project; keep `.cdsapirc` out of archives.
4. Validate all dates and generated ERA5 files before applying correction.

Keep the uncorrected MintPy products until the corrected HDF5 has been opened and checked. Record the hour, area, variables, pressure levels, date coverage, and tool versions in the run manifest.
