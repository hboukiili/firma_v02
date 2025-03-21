import ee
import geemap

# Authenticate with the service account
service_account = "gee-api-access@firma-452716.iam.gserviceaccount.com"
json_key_path = "/app/tools/sentinel_downloads/firma.json"

credentials = ee.ServiceAccountCredentials(service_account, json_key_path)
ee.Initialize(credentials)

# Define AOI (Area of Interest)
aoi = ee.Geometry.Polygon([
    [[-7.961307227350886, 32.72213445746634],
     [-7.961307227350886, 30.622146939353613],
     [-5.771570744294451, 30.622146939353613],
     [-5.771570744294451, 32.72213445746634],
     [-7.961307227350886, 32.72213445746634]]
])

# Define Date Range (PERSIANN-CDR is daily)
start_date = "2025-01-01"
end_date = "2025-02-28"

imerg = ee.ImageCollection('MSWEP V2.8 Global 3-hourly 0.1° Precipitation') \
    .filterBounds(aoi) \
    .filterDate(start_date, end_date) \
    # .select('precipitationCal')

count = imerg.size().getInfo()
print(count)
exit()
