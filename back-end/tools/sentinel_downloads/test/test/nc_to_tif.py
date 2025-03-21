import xarray as xr
import rioxarray
import rasterio
from rasterio.transform import Affine
import numpy as np

# --- Load and process LST data ---
ds = xr.open_dataset("LST_in.nc")
lst = ds["LST"]

# Replace _FillValue with NaN and apply scale/offset
fill_value = lst.attrs.get("_FillValue", None)
if fill_value is not None:
    lst = lst.where(lst != fill_value, np.nan)
scale_factor = lst.attrs.get("scale_factor", 1.0)
offset = lst.attrs.get("add_offset", 0.0)
lst = lst * scale_factor + offset

# Rename dimensions from 'rows','columns' to 'y','x'
lst = lst.rename({"rows": "y", "columns": "x"})

# --- Load geolocation data ---
geo_ds = xr.open_dataset("geodetic_in.nc")
lat = geo_ds["latitude_in"]
lon = geo_ds["longitude_in"]

# We assume lat and lon are 2D with shape (rows, columns). 
# For a regular grid, we can derive 1D coordinate arrays:
nrows, ncols = lat.shape

# Ensure the grid is oriented correctly:
# Check that latitude is descending (top row has highest value)
if lat.values[0, 0] < lat.values[-1, 0]:
    # Flip along vertical axis (y)
    lat = lat[::-1, :]
    lst = lst[::-1, :]

# Similarly, ensure that longitude increases left-to-right.
if lon.values[0, 0] > lon.values[0, -1]:
    lon = np.fliplr(lon.values)
    lst = lst.assign_coords(x=(("x"), np.flip(lst.x.values)))
else:
    lon = lon.values

# Compute 1D coordinates (assumes the grid is regular)
x_coords = np.linspace(lon[0, 0], lon[0, -1], ncols)
y_coords = np.linspace(lat.values[0, 0], lat.values[-1, 0], nrows)

# Assign these as coordinates for lst (overwriting the 2D ones)
lst = lst.assign_coords({"x": ("x", x_coords), "y": ("y", y_coords)})

# --- Compute the affine transform manually ---
# Use top-left corner from the 1D arrays:
x_min = x_coords[0]
y_max = y_coords[0]  # since y decreases downward, the first y is the top
pixel_width = (x_coords[-1] - x_coords[0]) / (ncols - 1)
pixel_height = (y_coords[0] - y_coords[-1]) / (nrows - 1)

# Create affine transform: note negative pixel_height since y decreases downward.
transform = Affine(pixel_width, 0, x_min,
                   0, -pixel_height, y_max)

# Write the computed transform and CRS to the DataArray.
lst.rio.write_transform(transform, inplace=True)
lst.rio.write_crs("EPSG:4326", inplace=True)

# --- Export to GeoTIFF ---
output_tif = "LST_output.tif"
lst.rio.to_raster(output_tif)

print("✅ Successfully converted NetCDF to GeoTIFF")
