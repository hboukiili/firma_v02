import rasterio
import numpy as np

def decode_QA_PIXEL(qa_pixel):
    """
    Decodes the Landsat QA_PIXEL band to produce a mask of valid pixels.
    
    Valid (1) pixels meet the following conditions:
      - Fill (bit 0) is 0.
      - Cloud Confidence (bits 3-4) is less than 2 (i.e. 0 or 1).
      - Cloud Shadow (bit 5) is 0.
      - Snow/Ice (bit 6) is 0.
      
    Invalid pixels (cloudy, cloud shadow, snow/ice, or fill) get a value of 0.
    """
    # Bit 0: Fill. (1 = fill/invalidate)
    fill = qa_pixel & 1
    # Bits 3-4: Cloud Confidence.
    cloud_conf = (qa_pixel >> 3) & 0b11  # values 0, 1, 2, or 3
    # Bit 5: Cloud Shadow.
    cloud_shadow = (qa_pixel >> 5) & 1
    # Bit 6: Snow/Ice.
    snow_ice = (qa_pixel >> 6) & 1

    # Valid pixels: no fill, cloud_confidence < 2, no cloud shadow, no snow/ice.
    valid = (fill == 0) & (cloud_conf < 2) & (cloud_shadow == 0) & (snow_ice == 0)
    return valid.astype(np.uint8)  # 1 for valid, 0 for invalid

# File paths (update these paths as needed)
red_file = "/app/tools/sentinel_downloads/m2m_data/Tensift/LC08_L2SP_202037_20240807_20240814_02_T1_SR_B4.TIF"    # Red band
nir_file = "/app/tools/sentinel_downloads/m2m_data/Tensift/LC08_L2SP_202037_20240807_20240814_02_T1_SR_B5.TIF"    # NIR band
qa_file  = "/app/tools/sentinel_downloads/m2m_data/Tensift/LC08_L2SP_202037_20240807_20240814_02_T1_QA_PIXEL.TIF"  # QA band
ndvi_output = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/20240814_NDVI.tif"  # Output NDVI file

# Open the datasets with rasterio
with rasterio.open(red_file) as src_red, \
     rasterio.open(nir_file) as src_nir, \
     rasterio.open(qa_file) as src_qa:
    
    # Copy metadata from the red band and update for output
    profile = src_red.profile.copy()
    profile.update(dtype=rasterio.float32, count=1, nodata=-9999)

    # Create the output NDVI file
    with rasterio.open(ndvi_output, 'w', **profile) as dst_ndvi:

        # Process the image in blocks (windows)
        for ji, window in src_red.block_windows(1):
            # Read the red, NIR, and QA bands for the current window
            red = src_red.read(1, window=window).astype(np.float32)
            nir = src_nir.read(1, window=window).astype(np.float32)
            qa = src_qa.read(1, window=window)

            # --- Apply Scaling for Landsat Surface Reflectance ---
            # For Landsat Collection 2, the scaling is: Reflectance = DN * 0.0000275 - 0.2
            red = red * 0.0000275 - 0.2
            nir = nir * 0.0000275 - 0.2

            # --- Clip Reflectance Values to 0-1 ---
            red = np.clip(red, 0, 1)
            nir = np.clip(nir, 0, 1)

            # --- Convert 0 Values to NoData (if 0 indicates no valid reflectance) ---
            red[red == 0] = -9999
            nir[nir == 0] = -9999

            # --- Decode the QA_PIXEL to get a validity mask ---
            valid_mask = decode_QA_PIXEL(qa)
            # Apply the mask: set invalid pixels to NaN
            red[valid_mask == 1] = -9999
            nir[valid_mask == 1] = -9999

            # --- NDVI Calculation ---
            ndvi = (nir - red) / (nir + red + 1e-10)  # Adding a small constant to avoid division by zero

            # --- Debug: Print NDVI min/max for this window ---
            print(f"Window {ji}: NDVI min = {np.nanmin(ndvi)}, max = {np.nanmax(ndvi)}")

            # Write the computed NDVI to the output file in the correct window
            dst_ndvi.write(ndvi.astype(np.float32), 1, window=window)

print("✅ Cloud-Free NDVI calculation completed and saved as", ndvi_output)
