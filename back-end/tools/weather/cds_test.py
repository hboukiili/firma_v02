import cdsapi
import xarray as xr
import io
import tempfile


c = cdsapi.Client(
    url= 'https://cds.climate.copernicus.eu/api',
    key= '127b99d4-1139-4059-9b83-594dc7e264dc'

)

# Retrieve the ERA5 reanalysis data for a specific region in memory
response = c.retrieve(
    'reanalysis-era5-single-levels',   # Specify the dataset
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',             # NetCDF format for better in-memory processing
        'variable': [
            'total_precipitation',           # Example variable: temperature at 2 meters
        ],
        'year': '2023',                 # Year
        'month': '08',                  # Month
        'day': '01',                    # Day
        'time': '12:00',                # Time
        'area': [
            32.2355, -7.9533             # Bounding box: [North, West, South, East]
        ],
    }
)

# Get the data in memory
data_bytes = io.BytesIO(response.download(target=None))

# Open the NetCDF dataset directly in memory using xarray
ds = xr.open_dataset(data_bytes)

# Now `ds` contains the dataset, and you can process it directly
print(ds)