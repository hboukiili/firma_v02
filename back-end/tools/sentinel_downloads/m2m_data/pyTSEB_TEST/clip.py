import rasterio
from rasterio.mask import mask
from shapely.geometry import Polygon, mapping
from pyproj import Transformer

lst_path = "/app/tools/sentinel_downloads/m2m_data/LST_CLOUD_FREE_Kelvin.tif"
ta_path  = "/app/tools/sentinel_downloads/m2m_data/ta_2m_temperature.tif"
u_path   = '/app/tools/sentinel_downloads/m2m_data/wind_speed_2m.tif'
new_lai  = f"/app/tools/sentinel_downloads/m2m_data/LAI.tif"

# Polygon coordinates in EPSG:4326 (lat/lon)
coords_str = '-7.680666 31.66665, -7.679964 31.666687, -7.679883 31.666271, -7.680436 31.666276, -7.680554 31.666536, -7.680666 31.66665'
coords_latlon = []
for pair in coords_str.split(','):
    lon, lat = map(float, pair.strip().split())
    coords_latlon.append((lon, lat))

# Set up a transformer from EPSG:4326 to EPSG:32629
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32629", always_xy=True)

# Transform each coordinate from lat/lon to the TIFF's CRS
coords_utm = [transformer.transform(lon, lat) for lon, lat in coords_latlon]

# Create the polygon in the TIFF's CRS
polygon = Polygon(coords_utm)
geojson_geom = [mapping(polygon)]

# Path to your input TIFF file (which is in EPSG:32629)
# input_tif = 'input.tif'
output_tif = 'lai_clipped_field.tif'

# Open the input TIFF file and apply the mask with the reprojected polygon
with rasterio.open(new_lai) as src:
    clipped_image, clipped_transform = mask(src, geojson_geom, crop=True)
    clipped_meta = src.meta.copy()

# Update metadata to reflect new dimensions and transform
clipped_meta.update({
    "driver": "GTiff",
    "height": clipped_image.shape[1],
    "width": clipped_image.shape[2],
    "transform": clipped_transform
})

# Write the clipped raster to disk
with rasterio.open(output_tif, "w", **clipped_meta) as dest:
    dest.write(clipped_image)

print("Clipped raster saved as:", output_tif)
