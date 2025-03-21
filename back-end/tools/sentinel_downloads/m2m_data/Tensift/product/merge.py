import rasterio
from rasterio.merge import merge
from rasterio.enums import Resampling
import glob
import numpy as np

# List all TIFF files to merge
tif_files = glob.glob("./lst/*.tif")

if not tif_files:
    raise FileNotFoundError("❌ No TIFF files found!")

# Open TIFF files
src_files = [rasterio.open(tif) for tif in tif_files]
print(src_files)
# Merge using 'first' or 'max' for better overlap handling
merged_array, merged_transform = merge(src_files, method="first")  # Change to 'max' if needed

# Convert NaN to NoData (-9999)
merged_array[np.isnan(merged_array)] = -9999

# Copy metadata and update for output
out_meta = src_files[0].meta.copy()
out_meta.update({
    "height": merged_array.shape[1],
    "width": merged_array.shape[2],
    "transform": merged_transform,
    "nodata": -9999,
    "driver": "GTiff",
    "compress": "LZW",
    "tiled": True
})

# Save merged file
with rasterio.open("./lst/merge.tif", "w", **out_meta) as dest:
    dest.write(merged_array)

print("✅ Merge completed and saved as merged.tif")
