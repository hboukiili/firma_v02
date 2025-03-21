import numpy as np
from osgeo import gdal, osr
import shutil
import gzip
import os

# === Step 1: Convert Binary to GeoTIFF ===
def persian_convert(input_file):

    file_name = input_file.split('.')[0]

    output_tiff = f"{file_name}.tif"  # GeoTIFF output
    output_fixed_tiff = f"fixed_{file_name}.tif"  # Longitude-corrected GeoTIFF

    # PDIR-NOW metadata
    rows, cols = 3000, 9000  # Confirmed shape
    dtype = np.float32  # Data format

    # Read binary data
    data = np.fromfile(input_file, dtype=dtype)

    # Ensure correct shape
    if data.size != rows * cols:
        raise ValueError(f"Unexpected file size: {data.size} elements, expected {rows*cols}")

    data = data.reshape((rows, cols))

    # Create GeoTIFF
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(output_tiff, cols, rows, 1, gdal.GDT_Float32)

    # Set projection (WGS84 - EPSG:4326)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dataset.SetProjection(srs.ExportToWkt())

    # Set georeferencing (0.04° resolution)
    lon_start, lat_start = 0, 60  # PDIR-NOW uses 0° to 360° longitude
    lon_res, lat_res = 0.04, -0.04
    dataset.SetGeoTransform([lon_start, lon_res, 0, lat_start, 0, lat_res])

    # Write data to raster band
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    band.SetNoDataValue(-9999)  # Preserve NoData value

    # Save and close
    dataset.FlushCache()
    dataset = None

    print(f"✅ Binary converted to GeoTIFF: {output_tiff}")
    
    # === Step 2: Shift Longitude from 0–360° to -180–180° ===
    dataset = gdal.Open(output_tiff, gdal.GA_ReadOnly)
    geoTransform = list(dataset.GetGeoTransform())

    # Check if longitude needs shifting
    if geoTransform[0] >= 0 and geoTransform[0] + geoTransform[1] * dataset.RasterXSize > 180:
        geoTransform[0] -= 180  # Shift left

    # Create new dataset with corrected longitude
    driver = gdal.GetDriverByName("GTiff")
    outDataset = driver.Create(output_fixed_tiff, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Float32)
    outDataset.SetGeoTransform(geoTransform)
    outDataset.SetProjection(dataset.GetProjection())

    # Copy data while preserving values
    band = dataset.GetRasterBand(1)
    outBand = outDataset.GetRasterBand(1)
    outBand.WriteArray(band.ReadAsArray())
    outBand.SetNoDataValue(-9999)

    # Close datasets
    outDataset.FlushCache()
    outDataset = None
    dataset = None

    print(f"✅ Longitude shifted and saved as: {output_fixed_tiff}")

    # === Step 3: Reproject to Google Maps (EPSG:3857) without Losing Values ===
    dataset_fixed = gdal.Open(output_fixed_tiff, gdal.GA_ReadOnly)

    gdal.Warp(output_tiff, dataset_fixed,
              dstSRS="EPSG:3857",  # Google Maps projection
              resampleAlg=gdal.GRA_NearestNeighbour,  # Preserve values without interpolation
              dstNodata=-9999)  # Keep NoData as -9999
    # os.remove(output_tiff)
    os.remove(output_fixed_tiff)
    print(f"✅ Reprojected to Google Maps (EPSG:3857) and saved as: {output_tiff}")
