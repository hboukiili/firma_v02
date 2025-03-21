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

# File paths
lst_file = "/app/tools/sentinel_downloads/m2m_data/Tensift/LC08_L2SP_203039_20240814_20240822_02_T1_ST_B10.TIF"  # LST (scaled) file
qa_file = "/app/tools/sentinel_downloads/m2m_data/Tensift/LC08_L2SP_203039_20240814_20240822_02_T1_QA_PIXEL.TIF"  # QA for clouds
output_file = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/A3_LST.tif"  # Output file for cloud-free LST in Kelvin

# Open the input datasets and prepare the output file using windowed processing
with rasterio.open(lst_file) as src_lst, rasterio.open(qa_file) as src_qa:
    profile = src_lst.profile.copy()
    # Update the profile for output: set dtype to float32 and nodata to np.nan
    profile.update(dtype=rasterio.float32, nodata=-9999)

    with rasterio.open(output_file, 'w', **profile) as dst:
        # Process the file in blocks to handle large files efficiently.
        for ji, window in src_lst.block_windows(1):
            # Read a chunk from the LST file (DN values)
            lst_dn = src_lst.read(1, window=window).astype(float)
            # Read the corresponding chunk from the QA file
            qa_pixel = src_qa.read(1, window=window)

            # Convert DN to LST in Kelvin only for nonzero DN values.
            # For DN == 0, assign nodata (np.nan) so that no conversion is performed.
            lst_kelvin = np.where(lst_dn == 0, -9999, (lst_dn * 0.00341802) + 149.0)

            valid_mask = decode_QA_PIXEL(qa_pixel)


            # Apply the cloud mask: set pixels flagged by the mask to nodata (np.nan)
            lst_kelvin[valid_mask == 1] = np.nan

            # Write the processed block to the output file
            dst.write(lst_kelvin.astype(np.float32), 1, window=window)

print(f"✅ Cloud-free LST (Kelvin) saved as {output_file}")
