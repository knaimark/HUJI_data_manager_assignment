The Python script `validate_data.py` performs data validation for the provided dataset `data_for_task.nc`. The dataset is from ERA5 hourly pressure level data. It is checked for **missing** and **out of range** values. 

The dataset contains data for:
- the date range between 2024-04-03 and 2024-04-05, hourly (72 values) 
- latitude between -20° to 20° in 0.25° increments (161 values)
- longitude between -10° to 10° in 0.25° increments (81 values)
- pressure levels of 1000, 550, 200, 20 and 1 hPa (5 values)

### Variable Thresholds Used in Validation

The typical ranges were defined according to the following table. Note that 1000 hPa pressure level roughly corresponds to sea level, and 1 hPa pressure level roughly corresponds to the altitude of 50 km.  

| Variable | Definition                  | Units                      | Range (min → max)      | Explanation |
|-----------|-----------------------------|-----------------------------|------------------------|--------------|
| d         | Divergence                  | 1/s                         | −10<sup>-3</sup> → 10<sup>-3</sup>           | Typical divergence does not exceed 10<sup>-4</sup>; up to 10<sup>-3</sup> in very strong jet-streaks. |
| cc        | Cloud cover                 | fraction (0–1)              | 0 → 1                  | Fractional cloud cover is always between 0 (clear) and 1 (fully cloudy). |
| z         | Geopotential                | m²/s²                       | −10<sup>4</sup> → 10<sup>6</sup>             | Corresponds to realistic geopotential heights from 500 m below sea level up to about 50 km altitude (geopotential equals geopotential height × g). |
| o3        | Ozone mass mixing ratio     | kg/kg                       | 0 → 10<sup>-4</sup>               | Typical ozone concentrations do not exceed 10<sup>-5</sup>. |
| pv        | Potential vorticity         | K·m²/(kg·s)                 | −10<sup>-4</sup>→ 10<sup>-4</sup>           | Typical potential vorticity is a few PVU (1 PVU = 10<sup>-6</sup> K·m²/(kg·s)), occasionally reaching 50 PVU. |
| r         | Relative humidity           | %                           | 0 → 100                | By definition, relative humidity cannot exceed 100% or fall below 0%. |
| ciwc      | Cloud ice water content     | kg/kg                       | 0 → 10<sup>-2</sup>               | Typically, does not exceed 2 g/kg or 2*10<sup>-3</sup> kg/kg. |
| clwc      | Cloud liquid water content  | kg/kg                       | 0 → 10<sup>-2</sup>               | Similar to ciwc. |
| q         | Specific humidity           | kg/kg                       | 0 → 1                  | Fractional quantity; realistic atmospheric values are much smaller (<0.1), but 1 is a safe upper bound. |
| crwc      | Cloud rain water content    | kg/kg                       | 0 → 10<sup>-2</sup>               | Similar to ciwc. |
| cswc      | Cloud snow water content    | kg/kg                       | 0 → 10<sup>-2</sup>              | Similar to ciwc. |
| t         | Temperature                 | K                           | 200 → 350              | Covers realistic atmospheric temperatures from hot surface conditions (say 50 °C or 320 K) to the 50 km altitude (around 270 K, sometimes dropping to 200-220 K). |
| u         | Eastward wind               | m/s                         | −150 → 150             | Highest value ever recorded is about 125 m/s. |
| v         | Northward wind              | m/s                         | −150 → 150             | Similar to u. |
| w         | Vertical velocity           | Pa/s                        | −5 → 5                 | Highest value ever recorded is about 3 Pa/s. |
| vo        | Relative vorticity          | 1/s                         | −10<sup>-2</sup> → 10<sup>-2</sup>           | Typically, up to 10<sup>-3</sup> even in extreme cases. |

### Data Validation Report 

Below is the summary of the results. No missing values were found. A significant portion of potential vorticity (19.6%) and relative humidity (6.4%) values fall outside their defined thresholds. This may indicate unrealistic threshold choices, measurement errors, reanalysis flaws, or data corruption. If the validity of these outliers is confirmed, they could also point to an interesting phenomenon worth further study. 
```
Variable   Definition                          Total    Missing    % Missing    Out-of-range      % Out
----------------------------------------------------------------------------------------------------   
d          Divergence                        4694760          0          0.0               0        0.0
cc         Cloud cover                       4694760          0          0.0               0        0.0
z          Geopotential                      4694760          0          0.0               0        0.0
o3         Ozone mass mixing ratio           4694760          0          0.0               0        0.0
pv         Potential vorticity               4694760          0          0.0          920335       19.6
r          Relative humidity                 4694760          0          0.0          299332        6.4
ciwc       Cloud ice water content           4694760          0          0.0               0        0.0
clwc       Cloud liquid water content        4694760          0          0.0               0        0.0
q          Specific humidity                 4694760          0          0.0               0        0.0
crwc       Cloud rain water content          4694760          0          0.0               0        0.0
cswc       Cloud snow water content          4694760          0          0.0               0        0.0
t          Temperature                       4694760          0          0.0               0        0.0
u          Eastward wind                     4694760          0          0.0               0        0.0
v          Northward wind                    4694760          0          0.0               0        0.0
w          Vertical velocity                 4694760          0          0.0               1        0.0
vo         Relative vorticity                4694760          0          0.0               0        0.0
```
### Proposed Next Steps

- Adjust threshold levels to make them more realistic
- Check basic consistency (temperature decreasing with pressure, latitude/longitude monotonicity) to rule out data corruption
- Check more advanced consistency, that is, relationships between different variables 
- Record the outlying values and map them onto the grid for further study
