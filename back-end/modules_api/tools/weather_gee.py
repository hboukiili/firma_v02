import ee
import math

class gee_data:

    def __init__(self, start_date, end_date, polygon) -> None:
        
        self.start_date = start_date
        self.end_date = end_date
        self.polygon = polygon

    def get_collection(self):

        self.collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
                        .filterBounds(self.polygon) \
                        .filterDate(self.start_date, self.end_date) \
                        .sort('system:time_start', True)
        
    
    def ws_calculation(self, image):

        u_band = image.select('u_component_of_wind_10m')
        v_band = image.select('v_component_of_wind_10m')

        u = u_band.reduceRegion(ee.Reducer.mean(), geometry=self.polygon, scale=10).get('u_component_of_wind_10m')
        v = v_band.reduceRegion(ee.Reducer.mean(), geometry=self.polygon, scale=10).get('v_component_of_wind_10m')

        u = ee.Number(u)
        v = ee.Number(v)

        wind_speed = u.pow(2).add(v.pow(2)).sqrt()

        wind_speed_value = wind_speed.getInfo()

        return wind_speed_value

    def Ta_calculation(self, image):
        
        Ta_band = image.select('temperature_2m').rename('Ta')
        mean_Ta = Ta_band.reduceRegion(ee.Reducer.mean(),
                    geometry=self.polygon, scale=10).get('Ta').getInfo() - 273.15
        
        return mean_Ta
    
    def rh_calculation(self, image):

        t_band = image.select('temperature_2m')
        d_band = image.select('dewpoint_temperature_2m')
    
        t = t_band.reduceRegion(ee.Reducer.mean(),
                geometry=self.polygon,
                scale=10).get('temperature_2m').getInfo() - 273.15
        d = d_band.reduceRegion(ee.Reducer.mean(),
                geometry=self.polygon,
                scale=10).get('dewpoint_temperature_2m').getInfo() - 273.15
    
        Rh = 100 * (math.exp((17.625 * d) / (243.04 + d)) / math.exp((17.625 * t) / (243.04 + t)))

        return Rh

    def Tdew_calculation(self, image):

        d_band = image.select('dewpoint_temperature_2m')
        d = d_band.reduceRegion(ee.Reducer.mean(), geometry=self.polygon, scale=10).get('dewpoint_temperature_2m').getInfo() - 273.15
        return d

    def Pre_calculation(self, image):

        Pre_band = image.select('total_precipitation')
        pre = Pre_band.reduceRegion(ee.Reducer.mean(), geometry=self.polygon, scale=10).get('total_precipitation').getInfo()
        return pre

    def get_weather_data(self):
        
        collection_size = self.collection.toList(self.collection.size()).getInfo()
        Ta, Ws, Tdew, pre, rh = [], [], [], [], []
        for image in collection_size:
            
            image = ee.Image(image['id'])
            timestamp = image.get('system:time_start').getInfo()
            print(timestamp)
            Ta.append([self.Ta_calculation(image), timestamp])
            Ws.append([self.ws_calculation(image), timestamp])
            Tdew.append([self.Tdew_calculation(image), timestamp])
            pre.append([self.Pre_calculation(image), timestamp])
            rh.append([self.rh_calculation(image), timestamp])
    
        return {
            'Temperature' : Ta,
            'WindSpeed' : Ws,
            'Tdew' : Tdew,
            'pre' : pre,
            'rh' : rh
        }
    


if __name__ == '__main__':

    service_account = 'firma-796@trencendece.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account,"cloud_credentials.json")
    ee.Initialize(credentials)

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
    ]])

    gee = gee_data('2018-01-01', '2018-01-31', polygon)

    gee.get_collection()
    print(gee.get_weather_data())