import ee
import os
import geemap

service_account = 'firma-796@trencendece.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, "cloud_credentials.json")
ee.Initialize(credentials)

# Define a point and buffer it to create a region
lat = 31.665358
long = -7.677980
point = ee.Geometry.Point([long, lat])

# Create a buffer around the point (e.g., 1 km)
region = point.buffer(1000)  # Buffer in meters

collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
                    .filterBounds(region) \
                    .filterDate('2024-01-10', '2024-05-31') \
                    .sort('system:time_start', True)

print("weather collection of images Number : ", collection.size().getInfo())

for image_info in collection.toList(collection.size()).getInfo():
    image = ee.Image(image_info['id'])

    hour_string = ee.Date(image.get('system:time_start')).format('HH').getInfo()
    date_string = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd').getInfo()

    base_dir = f"/home/hamza-boukili/Desktop/Lraba_blé_weather_date/{date_string}"
    if not os.path.exists(f"{base_dir}/pre"):
        os.makedirs(f"{base_dir}/pre")
    # os.makedirs(f"{base_dir}/v_w")
    # os.makedirs(f"{base_dir}/t2m")
    # os.makedirs(f"{base_dir}/dt2m")
    # os.makedirs(f"{base_dir}/ssrd")

    geemap.ee_export_image(image.select("total_precipitation_hourly").clip(region),
                           filename=f"{base_dir}/pre/{hour_string}.tif", scale=11132)
    # geemap.ee_export_image(image.select("dewpoint_temperature_2m").clip(region),
    #                        filename=f"{base_dir}/dt2m/{hour_string}.tif", scale=11132)
    # geemap.ee_export_image(image.select("temperature_2m").clip(region),
    #                        filename=f"{base_dir}/t2m/{hour_string}.tif", scale=11132)
    # geemap.ee_export_image(image.select("surface_solar_radiation_downwards").clip(region),
    #                        filename=f"{base_dir}/ssrd/{hour_string}.tif", scale=11132)
    # geemap.ee_export_image(image.select("v_component_of_wind_10m").clip(region),
    #                        filename=f"{base_dir}/v_w/{hour_string}.tif", scale=11132)
