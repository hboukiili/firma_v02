# import cdsapi

# # Initialize the CDS API client
# c = cdsapi.Client(
#     url= 'https://cds.climate.copernicus.eu/api',
#     key= '127b99d4-1139-4059-9b83-594dc7e264dc'

# )

# # Define the request
# c.retrieve(
#     'reanalysis-era5-single-levels',  # ERA5 Dataset
#     {
#         'product_type': 'reanalysis',
#         'variable': 'total_precipitation',  # Change variable as needed
#         'year': '2025',
#         'month': ['03'],  # March
#         'day': ['06'],  # Single day
#         'time': ['00:00', '06:00', '12:00', '18:00'],  # Specify times
#         'format': 'netcdf',  # File format
#         'area': [32.722134, -7.961307, 30.622146, -5.771570],  # Correct bounding box format [N, W, S, E]
#     },
#     'era5_precipitation.nc'  # Output file name
# )

# print("✅ ERA5 data successfully downloaded as 'era5_temperature.nc'.")

import xarray as xr

# Open the NetCDF file
ds = xr.open_dataset("era5_precipitation.nc")

# Print dataset information
print(ds)
