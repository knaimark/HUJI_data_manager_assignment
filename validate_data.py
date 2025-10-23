# `validate_data.py` is a Python script that validates ERA5 pressure-level data 
# stored in a NetCDF (.nc) file `data_for_task.nc`
# It checks for missing values and range violations

import xarray as xr
import numpy as np

# Load dataset
ds = xr.open_dataset("data_for_task.nc")
print("✅ Dataset loaded successfully")
# print(ds)

# Variable definitions (for report display)
var_defs = {
    "d":    "Divergence",
    "cc":   "Cloud cover",
    "z":    "Geopotential",
    "o3":   "Ozone mass mixing ratio",
    "pv":   "Potential vorticity",
    "r":    "Relative humidity",
    "ciwc": "Cloud ice water content",
    "clwc": "Cloud liquid water content",
    "q":    "Specific humidity",
    "crwc": "Cloud rain water content",
    "cswc": "Cloud snow water content",
    "t":    "Temperature",
    "u":    "Eastward wind",
    "v":    "Northward wind",
    "w":    "Vertical velocity",
    "vo":   "Relative vorticity"
}

# Define validation thresholds (typical ranges)
thresholds = {
    "d":    (-1e-3, 1e-3),     # Horizontal divergence [1/s]
    "cc":   (0, 1),            # Cloud cover [fraction]
    "z":    (-1e4, 1e6),       # Geopotential [m^2/s^2]
    "o3":   (0, 1e-4),         # Ozone mass mixing ratio [kg/kg]
    "pv":   (-1e-4, 1e-4),     # Potential vorticity [K m^2 / (kg s)]
    "r":    (0, 100),          # Relative humidity [%]
    "ciwc": (0, 1e-2),         # Cloud ice water content [kg/kg]
    "clwc": (0, 1e-2),         # Cloud liquid water content [kg/kg]
    "q":    (0, 1),            # Specific humidity [kg/kg] (fraction)
    "crwc": (0, 1e-2),         # Cloud rain water content [kg/kg]
    "cswc": (0, 1e-2),         # Cloud snow water content [kg/kg]
    "t":    (200, 350),        # Temperature [K]
    "u":    (-150, 150),       # Eastward wind [m/s]
    "v":    (-150, 150),       # Northward wind [m/s]
    "w":    (-5, 5),           # Vertical velocity [Pa/s]
    "vo":   (-1e-2, 1e-2)      # Relative vorticity [1/s]
}

# Validation loop
report = []

for var_name, da in ds.data_vars.items():
    data = da.values

    total = np.size(data)
    miss = np.isnan(data).sum()
    miss_pct = 100 * miss / total

    if var_name in thresholds:
        low, high = thresholds[var_name]
        out = ((data < low) | (data > high)).sum()
        out_pct = 100 * out / total
    else:
        print(f"⚠️ Range for '{var_name}' was not specified — 'out_of_range' set to NaN")
        out = np.nan
        out_pct = np.nan

    report.append((var_name, var_defs.get(var_name, "N/A"), total, miss, miss_pct, out, out_pct))

# Final summary table
print("\nDATA VALIDATION REPORT ")
print(f"{'Variable':<10} {'Definition':<30} {'Total':>10} {'Missing':>10} {'% Missing':>12} {'Out-of-range':>15} {'% Out':>10}")
print("-" * 100)

for var_name, desc, total, miss, miss_pct, out, out_pct in report:
    out_str = "N/A" if np.isnan(out) else f"{int(out)}"
    out_pct_str = "N/A" if np.isnan(out_pct) else f"{out_pct:10.1f}"
    print(f"{var_name:<10} {desc:<30} {total:>10} {miss:>10} {miss_pct:>12.1f} {out_str:>15} {out_pct_str:>10}")

print("\n✅ Validation complete")