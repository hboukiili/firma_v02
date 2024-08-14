import ee

service_account = 'firma-796@trencendece.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account,"cloud_credentials.json")
ee.Initialize(credentials)

# Define a polygon in Morocco (for example, around Marrakesh)
polygon = ee.Geometry.Polygon([
    [
        [
            -8.804708075796299,
            31.524806795903544
        ],
        [
            -8.80107552162903,
            31.523757995980716
        ],
        [
            -8.80089975287919,
            31.521910081750534
        ],
        [
            -8.804942434129487,
            31.52290895884667
        ],
        [
            -8.804883844546168,
            31.52478182461371
        ]
    ]
])

# List the contents of the folder to find the correct datasets

image = ee.Image("projects/earthengine-public/assets/ISDASOIL/Africa/v1/clay_content")

# print(image.getInfo())

ph_mean = image.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=polygon,
)

print(ph_mean.getInfo())

# image = ee.Image("projects/soilgrids-isric/sand_mean")

# sand_mean = image.reduceRegion(
#     reducer = ee.Reducer.mean(),
#     geometry= polygon
# )

# print(sand_mean.getInfo())

# image = ee.Image("projects/soilgrids-isric/silt_mean")

# sand_mean = image.reduceRegion(
#     reducer = ee.Reducer.mean(),
#     geometry= polygon
# )

# print(sand_mean.getInfo())

image = ee.Image("projects/soilgrids-isric/clay_mean")


sand_mean = image.reduceRegion(
    reducer = ee.Reducer.mean(),
    geometry= polygon
)

print(sand_mean.getInfo())

collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
    .filterBounds(polygon) \
    .filterDate('2018-01-01', '2018-05-01') \
    .sort('system:time_start', False)
    

# print(collection.getInfo())
for image in collection.toList(collection.size()).getInfo():

    image = ee.Image(image['id'])

    date_string_LANDSAT = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd-HH-mm').getInfo()
    
    Ta_band = image.select('temperature_2m').rename('Ta')

    mean_Ta = Ta_band.reduceRegion(ee.Reducer.mean(), geometry=polygon, scale=10).get('Ta').getInfo()

    print(date_string_LANDSAT, mean_Ta)