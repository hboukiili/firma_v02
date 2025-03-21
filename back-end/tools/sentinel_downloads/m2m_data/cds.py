import cdsapi
import xarray as xr
import io
import numpy as np
import rioxarray
from pyproj import Transformer

# -----------------------------
# Step 1: Convert UTM (EPSG:32632) to lat/lon (EPSG:4326)
# Provided bounding box (in meters):
# left = 492885.0, bottom = 3395385.0, right = 721515.0, top = 3628215.0
# transformer = Transformer.from_crs("EPSG:32629", "EPSG:4326", always_xy=True)

# # Your UTM bounds
# left, bottom, right, top = 492885.0, 3395385.0, 721515.0, 3628215.0

# Convert bottom-left and top-right corners
# lon_min, lat_min = transformer.transform(left, bottom)
# lon_max, lat_max = transformer.transform(right, top)

# ERA5 API expects [North, West, South, East] in lat/lon
# left = -9.85736     # lowerLeft longitude
# bottom = 30.71900    # lowerLeft latitude
# right = -7.20739    # upperRight longitude
# top = 32.16828
# # area = [left, bottom, right, top]
# area = [top, left, bottom, right]  # Correct order for CDS API

# print("Converted ERA5 area:", area)
# # -----------------------------
# # Step 2: Retrieve ERA5 Data using CDS API
# c = cdsapi.Client(
#     url='https://cds.climate.copernicus.eu/api',
#     key='127b99d4-1139-4059-9b83-594dc7e264dc'
# )

# response = c.retrieve(
#     'reanalysis-era5-single-levels',
#     {
#         'product_type': 'reanalysis',
#         'format': 'netcdf',
#         'variable': [
#             '2m_temperature',                # Temperature at 2 m (in Kelvin)
#             '10m_u_component_of_wind',       # 10 m U-component of wind (m/s)
#             '10m_v_component_of_wind'        # 10 m V-component of wind (m/s)
#         ],
#         'year': '2023',
#         'month': '08',
#         'day': '01',
#         'time': '12:00',
#         'area': area,
#     }
# )

# # # response.download(target=None) returns a file path (string)
# file_path = response.download(target=None)
# print("Downloaded file at:", file_path)

# -----------------------------
# Step 3: Open the NetCDF Data In-Memory Using xarray
file_path = 'ccfca1a03594e3826bffe2cc9dc62646.nc'
with open(file_path, 'rb') as f:
    data_bytes = io.BytesIO(f.read())

ds = xr.open_dataset(data_bytes)

# ERA5 data is provided in lat/lon; set the CRS to EPSG:4326.
ds = ds.rio.write_crs("EPSG:4326", inplace=True)

# -----------------------------
# Step 4: Save 2m Temperature as GeoTIFF
temp_tif = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/ta_2m_temperature.tif"
# '2m_temperature' is already in Kelvin.
ds['t2m'].rio.to_raster(temp_tif)
print("Saved 2m temperature (ta) as:", temp_tif)

# -----------------------------
# Step 5: Compute and Convert Wind Speed
# Calculate wind speed at 10 m from u and v components
u10 = ds['u10']
v10 = ds['v10']
wind_speed_10m = np.sqrt(u10**2 + v10**2)

# Convert 10 m wind speed to 2 m wind speed using a logarithmic wind profile:
# u(z) = u(10) * ln(z/z0) / ln(10/z0)
# Assume a roughness length, z0 = 0.03 m.
z0 = 0.03
conversion_factor = np.log(2 / z0) / np.log(10 / z0)  # ~0.723 for z0 = 0.03 m
wind_speed_2m = wind_speed_10m * conversion_factor

# Add the 2 m wind speed to the dataset
ds = ds.assign(wind_speed_2m=wind_speed_2m)

# -----------------------------
# Step 6: Save 2m Wind Speed as GeoTIFF
wind_tif = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/wind_speed_2m.tif"
ds['wind_speed_2m'].rio.to_raster(wind_tif)
print("Saved 2m wind speed as:", wind_tif)
