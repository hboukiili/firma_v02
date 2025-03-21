import zipfile
import os
import glob
import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
from osgeo import gdal

# Step 1: Unzip the folder
base_dir = "/app/tools/aquacrop_test/sentinel_data/zip_folders"
target = "/app/tools/aquacrop_test/sentinel_data/"

zip_files = glob.glob(os.path.join(base_dir, "*.zip"))

for zip_file in zip_files:
    unzip_dir = zip_file.split('.')[0]

    if not os.path.exists(unzip_dir):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)

    # Step 2: Identify and merge .jp2 files with the same resolution
    # directories = [d for d in os.listdir(unzip_dir) if os.path.isdir(os.path.join(unzip_dir, d))]

    # sub_directories = [d for d in os.listdir(f"{unzip_dir}/{directories[0]}/GRANULE") if os.path.isdir(os.path.join(f"{unzip_dir}/{directories[0]}/GRANULE", d))]

    
    # for folder in ["R10m", "R20m", "R60m"]:
        
    #     jp2_dir = os.path.join(unzip_dir, f"{unzip_dir}/{directories[0]}/GRANULE/{sub_directories[0]}/IMG_DATA/{folder}")
        

    #     # # Find all JP2 files in the directory
    #     jp2_files = glob.glob(os.path.join(jp2_dir, "*.jp2"))

    #     for file in jp2_files:
    #         if 'B' not in file.split('/')[-1]:
    #             jp2_files.remove(file)
    
    #     jp2_files = sorted(jp2_files)

    #     if folder == 'R20m' or folder == 'R60m':
    #         jp2_files.remove(jp2_files[-1])

    #     output_tif = f"{target}/{folder}/{unzip_dir.split('/')[-1]}.tif"

    #     src_ds = gdal.Open(jp2_files[0])
    #     cols = src_ds.RasterXSize
    #     rows = src_ds.RasterYSize
    #     proj = src_ds.GetProjection()
    #     geotransform = src_ds.GetGeoTransform()

    #     driver = gdal.GetDriverByName("GTiff")
    #     out_ds = driver.Create(output_tif, cols, rows, len(jp2_files), gdal.GDT_UInt16)

    #     # Set the projection and geotransform to the output file
    #     out_ds.SetProjection(proj)
    #     out_ds.SetGeoTransform(geotransform)

    #     for idx, jp2_file in enumerate(jp2_files):
    #         src_ds = gdal.Open(jp2_file)
    #         band = src_ds.GetRasterBand(1)
    #         band_data = band.ReadAsArray()
            
    #         # Write this band to the output file (bands are 1-indexed in GDAL)
    #         out_ds.GetRasterBand(idx + 1).WriteArray(band_data)

    #     out_ds.FlushCache()  # Save to disk
    #     out_ds = None  # Close the file
    #     print(f"Successfully created multi-band TIFF: {output_tif}")
