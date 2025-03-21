import rasterio
import numpy as np

ndvi_file = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/clipped_tensift.tif"  # Input NDVI file
fc_output = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/FC.tif"  # Output Fractional Vegetation Cover file
lai_output = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/LAI.tif"  # Output Leaf Area Index file

NDVIv = 0.95
NDVIs = 0.05
k = 0.5 

with rasterio.open(ndvi_file) as src_ndvi:
    profile = src_ndvi.profile.copy()
    nodata_value = src_ndvi.nodata if src_ndvi.nodata is not None else np.nan

    profile.update(dtype=rasterio.float32, count=1, nodata=nodata_value)

    with rasterio.open(fc_output, 'w', **profile) as dst_fc, \
         rasterio.open(lai_output, 'w', **profile) as dst_lai:

        for ji, window in src_ndvi.block_windows(1):
            ndvi = src_ndvi.read(1, window=window).astype(np.float32)

            if np.isnan(nodata_value):
                nodata_mask = np.isnan(ndvi)
            else:
                nodata_mask = ndvi == nodata_value

            fc = (ndvi - NDVIs) / (NDVIv - NDVIs)
            fc = np.clip(fc, 0, 1)
            fc = fc ** 2

            lai = -np.log(1 - fc + 1e-10) / k

            fc[nodata_mask] = nodata_value
            lai[nodata_mask] = nodata_value

            dst_fc.write(fc.astype(np.float32), 1, window=window)
            dst_lai.write(lai.astype(np.float32), 1, window=window)

with rasterio.open(fc_output) as dst_fc, rasterio.open(lai_output) as dst_lai:
    fc = dst_fc.read(1)
    lai = dst_lai.read(1)

    print(f"FC bounds: {dst_fc.bounds}")
    print(f"FC min = {np.nanmin(fc)}, max = {np.nanmax(fc)}")
    print(f"LAI min = {np.nanmin(lai)}, max = {np.nanmax(lai)}")

print("Fractional Vegetation Cover (FC) and LAI calculation completed and saved.")
