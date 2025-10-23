# `download_data.py` is a Python script that downloads the required data from the CDS database
# That is, it downloads the ERA5 Renalysis hourly single-level data for: 
# - July 15 2024 (one-day subset) 
# - 1°×1° box around Jerusalem
# - the variables are `2m_temperature`, `2m_dewpoint_temperature`, `surface_pressure`, `mean_sea_level_pressure`, 
#   `10m_u_component_of_wind`, `10m_v_component_of_wind`, and `total_precipitation`

# Load the module `cdsapi` into memory 
# This is the Python interface that allows the script to talk to the CDS database
# rather than get the data manually  
import cdsapi

# Define the dataset that we need from the CDS 
# Its name is defined in the CDS database according to what data we want
dataset = "reanalysis-era5-single-levels"

# Define the common parameters (date, location, the type of the target file)
common_request = {
    "product_type": ["reanalysis"],
    "year": ["2024"],
    "month": ["07"],
    "day": ["15"],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [32.28, 34.72, 31.28, 35.72]
}

# Define the list of variables
variables = [
    "2m_temperature",
    "2m_dewpoint_temperature",
    "surface_pressure",
    "mean_sea_level_pressure",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "total_precipitation"
]
 
# Create a client - that's an object that knows how to talk to the CDS
# In particular, it reads my CDS credentials from the hidden file `.cdsapirc`
client = cdsapi.Client()

# Retrieve each variable separately and save to its own .nc file such as `era5_jerusalem_2m_temperature.nc`
for var in variables:
    request = common_request.copy()
    request["variable"] = [var]

    target_file = f"era5_jerusalem_{var}.nc"
    print(f"⬇️ Downloading {var} → {target_file}")
    
    client.retrieve(dataset, request, target_file)

print("✅ All variables for 2024-07-15 around Jerusalem downloaded successfully.")    