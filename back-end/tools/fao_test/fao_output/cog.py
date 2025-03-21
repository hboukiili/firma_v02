from osgeo import gdal
import os
gdal.UseExceptions()

def convert_tif_to_cog(input_tif, output_cog, compress="DEFLATE", tile_size=512):
    """
    Convert a GeoTIFF to a Cloud Optimized GeoTIFF (COG).
    Args:
        input_tif (str): Path to the input TIFF file.
        output_cog (str): Path to the output COG file.
        compress (str): Compression type (e.g., DEFLATE, JPEG).
        tile_size (int): Block size in pixels (e.g., 512).
    """
    # Prepare creation options (no OVERVIEWS or TILED)
    options = [
        f"COMPRESS={compress}",
        "ADD_OVERVIEWS=NO"  # Disable overviews
    ]
    
    # Translate the GeoTIFF to COG
    try:

        gdal.Translate(
            output_cog,
            input_tif,
            format="COG",
            outputType=gdal.GDT_Float32,  # Match original data type
            creationOptions=options
        )
        print(f"Converted {input_tif} to {output_cog} as COG.")
    except RuntimeError as e:
        print(f"An error occurred: {e}")
# Example usage


# for folder in folders:
var = f"/app/tools/aquacrop_test/sentinel_data/ndvi"
files = [f for f in os.listdir(var) if os.path.isfile(os.path.join(var, f))]
for file in files:
    convert_tif_to_cog(f"{var}/{file}", f"{var}_cog/cog_{file}")
    break
