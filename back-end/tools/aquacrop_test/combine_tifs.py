import rasterio
from rasterio.enums import Resampling
import glob
import os
import numpy as np

# Directory containing the TIF files

# List all TIF files
# tif_files = sorted(glob.glob(os.path.join(tif_dir, "*.tif")))

# Open the first TIF to get metadata
# with rasterio.open(tif_files[0]) as src0:
#     meta = src0.meta

# # Update the metadata to reflect the number of layers
# meta.update(count=1)

# # Define output path

# # Create an empty array to accumulate the data
# combined_data = np.zeros((meta['height'], meta['width']), dtype=meta['dtype'])

# # # Loop through the TIF files and sum the data
# for tif in tif_files:
#     with rasterio.open(tif) as src:
#         data = src.read(1)  # Read the first band
#         combined_data += data

# # Write the combined data to a new single-band TIF
# with rasterio.open(output_path, "w", **meta) as dst:
#     dst.write(combined_data, 1)
# import rasterio
# import glob
# import os

# Directory containing the TIF files
# tif_dir = "/home/hamza-boukili/Desktop/Chichaoua_olivier/2022-03-01/dt2m"

# # List all TIF files
# tif_files = sorted(glob.glob(os.path.join(tif_dir, "*.tif")))

# # Open the first TIF to get metadata
# with rasterio.open(tif_files[0]) as src0:
#     meta = src0.meta

# # Update metadata to reflect the number of layers (24 bands for 24 hours)
# meta.update(count=len(tif_files))

# # Define the output path for the combined multi-band TIF
output_path = "/app/tools/aquacrop_test/combined_output.tif"

# # Write the combined multi-band TIF
# with rasterio.open(output_path, "w", **meta) as dst:
#     for id, tif in enumerate(tif_files, start=1):
#         with rasterio.open(tif) as src:
#             dst.write_band(id, src.read(1))

# print("Multi-band TIF created successfully.")

with rasterio.open(output_path) as src:
    print(f"Number of bands: {src.count}")
    print(f"Width: {src.width}, Height: {src.height}")
    print(f"CRS: {src.crs}")
    print(f"Transform: {src.transform}")

    # Read a specific band (e.g., band 1 representing hour 00:00-01:00)
    band1 = src.read(1)

    # Print statistics or inspect data
    print(band1)