import xarray as xr
import rasterio
from rasterio.transform import from_bounds

# File paths
lst_file = "LST_in.nc"
geo_file = "geodetic_in.nc"

# Load the datasets
lst_data = xr.open_dataset(lst_file)
geo_data = xr.open_dataset(geo_file)

# Extract the LST variable and convert from Kelvin to Celsius
lst = lst_data['LST'] - 273.15  # Convert Kelvin to Celsius

# Print metadata to check the units
print("LST metadata:", lst_data['LST'].attrs)

# Extract latitude and longitude from the geodetic dataset
longitude = geo_data['longitude_in']
latitude = geo_data['latitude_in']

# Define the transform using bounds and resolution from the geodetic file
transform = from_bounds(
    west=longitude.min().values,  # Minimum longitude
    east=longitude.max().values,  # Maximum longitude
    south=latitude.min().values,  # Minimum latitude
    north=latitude.max().values,  # Maximum latitude
    width=lst.shape[1],           # Number of columns
    height=lst.shape[0],          # Number of rows
)

# Flip the LST data vertically to correct for the north-south inversion.
lst_flipped = lst[::-1, :]

# Output file path
output_tiff = "LST_output_v7.tif"

# Write the flipped data to a GeoTIFF using the computed transform
with rasterio.open(
    output_tiff,
    'w',
    driver='GTiff',
    height=lst_flipped.shape[0],
    width=lst_flipped.shape[1],
    count=1,  # one band
    dtype=lst_flipped.dtype,
    crs="EPSG:4326", 
    transform=transform,
) as dst:
    dst.write(lst_flipped.values, 1)

print(f"GeoTIFF saved to {output_tiff}")
