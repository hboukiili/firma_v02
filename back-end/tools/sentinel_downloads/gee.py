import geemap
import ee

# Path to your service account JSON file
service_account = "gee-api-access@firma-452716.iam.gserviceaccount.com"
json_key_path = "./firma.json"

# Authenticate with the service account
credentials = ee.ServiceAccountCredentials(service_account, json_key_path)
ee.Initialize(credentials)

# print("GEE Authentication Successful!")


def calculate_lst(image):
    # Select Thermal Band 10 (TIRS1) and apply scale factor
    thermal = image.select("ST_B10").multiply(0.00341802).add(149.0)

    # Convert to LST using emissivity correction (Assuming NDVI-based estimation)
    ndvi = image.normalizedDifference(["SR_B5", "SR_B4"])  # NDVI = (NIR - RED) / (NIR + RED)
    pv = ndvi.multiply(ndvi)  # Proportion of Vegetation
    emissivity = pv.multiply(0.004).add(0.986)  # Emissivity

    lst = thermal.divide(emissivity)  # Apply emissivity correction
    return lst.rename("LST")  # Rename to LST


# Define Area of Interest (AOI) using Latitude and Longitude
aoi = ee.Geometry.Polygon([
        [492885.0, 3395385.0],
        [721515.0, 3395385.0],
        [721515.0, 3628215.0],
        [492885.0, 3628215.0],
        [492885.0, 3395385.0]
      ])

start_date = "2024-03-01"
end_date = "2024-03-31"

# Load ERA5 HOURLY ImageCollection for the specified period and AOI
era5 = ee.ImageCollection("ECMWF/ERA5/HOURLY") \
    .filterBounds(aoi) \
    .filterDate(start_date, end_date) \
    .map(lambda image: image.clip(aoi))  # Clip the image to AOI

# Compute the mean image over the period
era5_mean = era5.mean()

# Correct band names: ERA5 uses 'temperature_2m'
ta = era5_mean.select('temperature_2m').rename('Ta')

# Use the correct wind component names:
u_wind = era5_mean.select('u_component_of_wind_10m')
v_wind = era5_mean.select('v_component_of_wind_10m')
wind_speed = u_wind.pow(2).add(v_wind.pow(2)).sqrt().rename('wind_speed')

# Define export parameters (ERA5 resolution is coarse, so we use a larger scale)
scale = 3000  # Approximate scale in meters

output_ta = "./Data/Ta_ERA5.tif"
output_wind_speed = "./Data/wind_speed_ERA5.tif"

# Export the images locally
try:
    geemap.ee_export_image(ta, filename=output_ta, scale=scale, region=aoi, file_per_band=False)
    # geemap.ee_export_image(wind_speed, filename=output_wind_speed, scale=scale, region=aoi, file_per_band=False)
    print("Export completed: Ta and wind_speed images saved locally.")
except Exception as e:
    print("Error exporting ERA5 images:", e)

# # Define the date range for downloading data
# start_date = "2024-02-01"
# end_date = "2024-02-20"

# # Load Landsat 8 Collection 2 Level-2 (Surface Reflectance & Thermal Bands)
# landsat = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
#     .filterBounds(aoi) \
#     .filterDate(ee.Date(start_date), ee.Date(end_date)) \
#     # .map(lambda image: image.clip(aoi))  # Clip the image to AOI

# # Select the first image available in the filtered dataset
# # print(landsat.first().getInfo())
# image = landsat.first()

# # Print Image ID
# print("Selected Image ID:", image.get("system:id").getInfo())


# lst_image = calculate_lst(image)# Print min/max temperature values

# print(lst_image.reduceRegion(ee.Reducer.minMax(), aoi, 30).getInfo())
# ndvi = image.normalizedDifference(["SR_B5", "SR_B4"]).rename("NDVI")

# # Calculate LAI from NDVI using an empirical relationship
# lai = ndvi.expression(
#     '-log((0.69 - ndvi) / 0.59) / 0.91', {
#         'ndvi': ndvi
#     }).rename("LAI")

# # Define export parameters
# scale = 30  # Landsat 8 native resolution

# output_ndvi = "./Data/NDVI_Landsat8.tif"
# output_lst  = "./Data/LST_Landsat8.tif"
# output_lai  = "./Data/LAI_Landsat8.tif"

# # Export the images locally
# try:
#     # geemap.ee_export_image(lst_image, filename=output_lst, scale=scale, region=aoi, file_per_band=False)
#     # geemap.ee_export_image(ndvi, filename=output_ndvi, scale=scale, region=aoi, file_per_band=False)
#     geemap.ee_export_image(lai, filename=output_lai, scale=scale, region=aoi, file_per_band=False)
#     print("Download completed! Files saved locally.")
# except Exception as e:
#     print(f"Error exporting image: {e}")

# # Initialize Google Earth Engine
# # ee.Initialize()

# # Define your AOI polygon
# aoi = ee.Geometry.Polygon([
#           [
#             [
#               -6.392481862309893,
#               32.395346891622594
#             ],
#             [
#               -6.392481862309893,
#               32.38200039435689
#             ],
#             [
#               -6.375682559483977,
#               32.38200039435689
#             ],
#             [
#               -6.375682559483977,
#               32.395346891622594
#             ],
#             [
#               -6.392481862309893,
#               32.395346891622594
#             ]
#           ]
#         ])

# # Load Landsat 8 Collection
# image = (ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
#          .filterBounds(aoi)
#          .filterDate('2024-03-01', '2024-03-31')  # Modify date as needed
#         #  .sort('CLOUD_COVER')
#          .first())

# # Compute NDVI
# ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
# # Get image projection info
# pixel_count = ndvi.reduceRegion(
#     reducer=ee.Reducer.count(),
#     geometry=aoi,
#     scale=30,
#     maxPixels=1e13
# ).getInfo()

# num_pixels = pixel_count.get('NDVI', 0)  # Get NDVI count or 0 if missing

# # Compute file size in GB (32-bit float means 4 bytes per pixel)
# bit_depth = 32
# size_bytes = num_pixels * (bit_depth / 8)
# size_gb = size_bytes / (10**9)

# print(f"Estimated NDVI Image Size: {size_gb} GB")

# thermal = image.select('B10')  # Thermal Infrared Band 10
# K1, K2 = 774.89, 1321.08  # Landsat 8 Thermal Constants

# # Compute TOA Radiance (L)
# L = thermal.multiply(0.0003342).add(0.1)

# # Correct brightness temperature calculation:
# BT = ee.Image(K2).divide(ee.Image(K1).divide(L).add(1).log())

# # Convert BT from Kelvin to Celsius
# lst = calculate_lst(image)

# # Compute LAI from NDVI
# lai = ndvi.expression(
#     '-log((0.69 - ndvi) / 0.59) / 0.91', {
#         'ndvi': ndvi
#     }).rename('LAI')



# #  Download at 30m resolution
# scale = 30  # Landsat 8 native resolution

# #  Export images locally
# try :
#     # url = ndvi.getDownloadURL({
#     # 'scale': 30,
#     # 'region': aoi,
#     # 'format': 'GEO_TIFF'
#     # })
#     # print("Download URL:", url)
#     # geemap.ee_export_image(ndvi, filename=output_ndvi, scale=scale, region=aoi, file_per_band=False)
#     geemap.ee_export_image(lst, filename=output_lst, scale=scale, region=aoi, file_per_band=False)
#     geemap.ee_export_image(lai, filename=output_lai, scale=scale, region=aoi, file_per_band=False)
#     print("Download completed! Files saved locally.")
# except Exception as e:
#     print(f"Error exporting image: {e}")
