# PART 1 - DOWNLOADING ERA5 DATA
The Python script `download_data.py` downloads **ERA5 Reanalysis hourly single-level data** for a **1°×1° box around Jerusalem** on **2024-07-15** using the **CDS API**. It retrieves 2m temperature and dewpoint, surface and mean sea level pressure, 10m wind components, and total precipitation. The script saves the data in **NetCDF** format. Each variable is saved in its own file such as `era5_jerusalem_2m_temperature.nc`.

### Requirements
- Python 3.10 or higher
- Python packages `cdsapi`, `xarray`, `netCDF4` (install using `pip install cdsapi xarray netcdf4`)
- Built-in modules: `os`
- A valid **CDS API key** configured in `~/.cdsapirc` 

# PART 2 - CREATING A DATABASE THAT SUPPORTS SIMILAR ERA5 DOWNLOADS
The Python script `models.py` defines a relational database named `era5.db` that handles requests similar to the one in `download_data.py`. It supports storing and tracking downloaded ERA5 Reanalysis hourly single-level data for: 
- a certain date (a one-day subset)
- a 1°×1° box around certain location
- a specified list of variables

The script implements **`era5_ERD`** using **SQLAlchemy ORM**. The schema allows the database to: 
- Prevent redundant downloads by identifying data already stored locally
- Support efficient queries by date, location, and variable  

### Requirements
- Python 3.10 or higher
- Python package `sqlalchemy` (install using `pip install sqlalchemy`)

### Example of Usage
```python
    from sqlalchemy import create_engine
    from models import Base
    # Create an SQLite database era5
    engine = create_engine("sqlite:///era5.db")
    # Create tables defined in models.py
    Base.metadata.create_all(engine)
```
### Key Assumptions, Known Limitations, and Proposed Next Steps
| **Key Assumptions** | **Known Limitations** | **Proposed Next Steps** |
| :---                | :---                  | :---                    |
|Only **hourly single-level** ERA5 data are handled|No pressure-level or monthly-mean data|Extend support to additional ERA5 data types|
|Each dataset covers a **single date**|Multi-day ranges not supported|Extend support for multi-day ranges       |
|Each dataset covers a **1°×1° box** around a location|Multi-location datasets not supported|Extend support to multiple or larger spatial domains|
|Each file stores **one variable only**|Separate CDS requests per variable are slower than combined request|Implement multi-variable downloads with automatic file splitting|
|Files are stored **locally**|No support for remote/cloud file paths|Add support for remote/cloud storage|
|Download script and database are **not linked**|New downloads must be added manually|Implement automatic database updates after downloads|
|Interaction is **manual**|No user interface|Develop UI/dashboard for downloads/queries| 