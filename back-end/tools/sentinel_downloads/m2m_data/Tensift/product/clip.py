# import json

# import json
# import geopandas as gpd
# from shapely.geometry import Polygon, MultiPolygon

# # Load the GeoJSON file
# with open("/app/tools/shapeFile.geojson") as f:
#     geojson_data = json.load(f)

# # Extract the polygon for 'Tensift'
# geojson_polygons = []
# for feature in geojson_data["features"]:
#     if feature['properties'].get('Bassin') == 'Tensift':
#         Tensift = feature['geometry']['coordinates']
#         break  # Stop after finding the correct feature

# # Convert to a Shapely Polygon
# tensift_polygon = MultiPolygon(Tensift)  # Take the first list if it's MultiPolygon

# # Convert to GeoDataFrame for compatibility
# gdf = gpd.GeoDataFrame({"geometry": [tensift_polygon]}, crs="EPSG:4326")

# # Save the clipped shape as a new GeoJSON file
# gdf.to_file("tensift_clip.geojson", driver="GeoJSON")

# print("✅ Tensift polygon extracted and saved as 'tensift_clip.geojson'")


# import geopandas as gpd

# # Load the GeoJSON file (assumed to be in EPSG:4326)
# gdf = gpd.read_file("tensift_clip.geojson")

# # Reproject to match the raster's CRS (EPSG:32629)
# gdf = gdf.to_crs("EPSG:32629")

# # Save the reprojected GeoJSON
# gdf.to_file("tensift_clip_32629.geojson", driver="GeoJSON")

# print("✅ GeoJSON reprojected to EPSG:32629 and saved as 'tensift_clip_32629.geojson'")

# import rasterio
# from rasterio.mask import mask

# # Open the GeoJSON file
# tensift_gdf = gpd.read_file("tensift_clip_32629.geojson")

# # Extract geometry
# geometry = tensift_gdf.geometry.values

# # Open the merged TIFF
# with rasterio.open("/app/tools/sentinel_downloads/m2m_data/Tensift/product/ta_2m_temperature.tif") as src:
#     clipped_array, clipped_transform = mask(src, geometry, crop=True)

#     # Update metadata
#     out_meta = src.meta.copy()
#     out_meta.update({
#         "height": clipped_array.shape[1],
#         "width": clipped_array.shape[2],
#         "transform": clipped_transform
#     })

# # Save the clipped output
# with rasterio.open("t2m.tif", "w", **out_meta) as dest:
#     dest.write(clipped_array)

# print("✅ Clipping completed and saved as clipped_tensift.tif")

import rasterio
import numpy as np

# Input and Output file paths
input_tif = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/t2m.tif"  # Replace with your file
output_tif = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/t2m.tif"  # Output file with NoData

# Open the TIFF file
with rasterio.open(input_tif) as src:
    profile = src.profile.copy()  # Copy metadata
    data = src.read(1)  # Read the first band (adjust for multi-band)

    # Set 0 values to NoData
    nodata_value = -9999  # You can also use another NoData value
    data[np.isnan(data)] = nodata_value
    print(data)
    # Update metadata
    profile.update(dtype=rasterio.float32, nodata=nodata_value)

#     # Save the updated file
    with rasterio.open(output_tif, 'w', **profile) as dst:
        dst.write(data.astype(np.float32), 1)

print(f"✅ Converted 0 values to NoData and saved as: {output_tif}")