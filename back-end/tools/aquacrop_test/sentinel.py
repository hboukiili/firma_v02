
from datetime import date, timedelta
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import os
import rasterio
from rasterio.enums import Resampling

pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns

copernicus_user = "hm.boukiili97@gmail.com"
copernicus_password = "Mas123456789@"
ft = "POLYGON((-7.678419088737144 31.66600208716224, -7.677561484332273 31.665936327983204, -7.677461044176198 31.664400837917725, -7.678434541068782 31.664367957767254, -7.678430677985574 31.66598564737157, -7.678419088737144 31.66600208716224))"
data_collection = "SENTINEL-2" # Sentinel satellite

# today =  "2018-02-01"
today_string = "2024-01-15"
# yesterday 
yesterday_string = "2024-01-10"



def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
        )
    return r.json()["access_token"]

base_dir = "/app/tools/aquacrop_test/sentinel_data/"
# json_ = requests.get(
#     f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{ft}') and ContentDate/Start gt {yesterday_string}T00:00:00.000Z and ContentDate/Start lt {today_string}T00:00:00.000Z&$count=True&$top=1000"
# ).json()  
# p = pd.DataFrame.from_dict(json_["value"]) # Fetch available dataset
# # print(p)
# if p.shape[0] > 0 :
#     p["geometry"] = p["GeoFootprint"].apply(shape)
#     productDF = gpd.GeoDataFrame(p).set_geometry("geometry") # Convert PD to GPD
#     productDF = productDF[~productDF["Name"].str.contains("L1C")] # Remove L1C dataset
#     print(f" total L2A tiles found {len(productDF)}")
#     productDF["identifier"] = productDF["Name"].str.split(".").str[0]
#     allfeat = len(productDF) 
#     if allfeat == 0:
#         print("No tiles found for today")
#     else:
#         ## download all tiles from server
#         for index,feat in enumerate(productDF.iterfeatures()):
#             # try:
#                 session = requests.Session()
#                 keycloak_token = get_keycloak(copernicus_user,copernicus_password)
#                 session.headers.update({"Authorization": f"Bearer {keycloak_token}"})

#                 product_id = feat["properties"]["Id"]
#                 metadata_url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/Nodes"
#                 metadata_response = session.get(metadata_url)
#                 print('got the metadata...')
#                 if metadata_response.status_code == 200:
#                     metadata_json = metadata_response.json()
#                     nodes_uri = metadata_json['result'][0]['Nodes']['uri']
#                     print('Got the uri ..')
#                     nodes_response = session.get(nodes_uri)
#                     for i in nodes_response.json()['result']:
#                         if i['Name'] == 'GRANULE':
#                             uri = i['Nodes']['uri']
#                             print('Got GRANULE uri')
#                             granule_reponse = session.get(uri)
#                             folder_uri = granule_reponse.json()['result'][0]['Nodes']['uri']
#                             folder_response = session.get(folder_uri)
#                             for x in folder_response.json()['result']:
#                                 if x['Name'] == 'IMG_DATA':
#                                     print('got the ING data uri')
#                                     uri = x['Nodes']['uri']
#                                     band_folder_reponse = session.get(uri)
#                                     for x in band_folder_reponse.json()['result']:
#                                         path = f"{base_dir}{x['Name']}"
#                                         if not os.path.exists(path):
#                                             os.makedirs(path)
            
#                                         band = x['Nodes']['uri']
#                                         band_folder = session.get(band)
#                                         for jp2_file in band_folder.json()['result']:

#                                             # print(jp2_file)
#                                             if jp2_file['Name'].endswith('.jp2'):
                
#                                                 jp2_uri = jp2_file['Nodes']['uri']
#                                                 print(f"Downloading {jp2_file['Name']}...")
#                                                 print(jp2_uri)
#                                                 jp2_response = session.get(jp2_uri)

#                                                 if jp2_response.status_code == 200:

#                                                     print(jp2_response.content)
#                                                     exit(1)
                                                    # jp2_filename = jp2_file['Name']
                                                    # with open(f"{path}/{jp2_filename}", 'wb') as f:
                                                    #     f.write(jp2_response.content)
                                                    #     tif_filename = jp2_filename.replace('.jp2', '.tif')
                                                    # with rasterio.open(jp2_filename) as src:
                                                    #     data = src.read(
                                                    #         out_shape=(
                                                    #             src.count,
                                                    #             src.height,
                                                    #             src.width
                                                    #         ),
                                                    #         resampling=Resampling.bilinear
                                                    # )

                                                    # profile = src.profile
                                                    # profile.update(
                                                    #     driver='GTiff',
                                                    #     dtype=rasterio.uint16,
                                                    #     count=1,
                                                    #     compress='lzw'
                                                    # )

                                                    # with rasterio.open(tif_filename, 'w', **profile) as dst:
                                                    #     dst.write(data, 1)
                                                    
                                                    # print(f"Saved {tif_filename}")
                                                    # exit(1)
                                                    # os.remove(jp2_filename)

# else :
#     print('no data found')

json_ = requests.get(
    f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{ft}') and ContentDate/Start gt {yesterday_string}T00:00:00.000Z and ContentDate/Start lt {today_string}T00:00:00.000Z&$count=True&$top=1000"
).json()  
p = pd.DataFrame.from_dict(json_["value"]) # Fetch available dataset
if p.shape[0] > 0 :
    p["geometry"] = p["GeoFootprint"].apply(shape)
    Tile_ID = p["Name"].str.extract(r"(T\d{2}[A-Z]{3})").values[0]

    print(Tile_ID)  # Tile names and IDs
    productDF = gpd.GeoDataFrame(p).set_geometry("geometry") # Convert PD to GPD
    productDF = productDF[~productDF["Name"].str.contains("L1C")] # Remove L1C dataset
    print(f" total L2A tiles found {len(productDF)}")
    productDF["identifier"] = productDF["Name"].str.split(".").str[0]
    allfeat = len(productDF) 
    # print(productDF)
    # print('done')
    # if allfeat == 0:
    #     print("No tiles found for today")
    # else:
    #     ## download all tiles from server
    #     for index,feat in enumerate(productDF.iterfeatures()):
    #         # print(index, feat['properties']['OriginDate'].split('T')[0])
    #         # break 
    #         try:
    #             session = requests.Session()
    #             keycloak_token = get_keycloak(copernicus_user,copernicus_password)
    #             session.headers.update({"Authorization": f"Bearer {keycloak_token}"})
    #             url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({feat['properties']['Id']})/$value"
    #             response = session.get(url, allow_redirects=False)
    #             print('got Response ...')
    #             while response.status_code in (301, 302, 303, 307):
    #                 print('redirected ...')
    #                 url = response.headers["Location"]
    #                 response = session.get(url, allow_redirects=False)
    #             print('start downlaoding : ', feat['properties']['OriginDate'].split('T')[0])
    #             file = session.get(url, verify=False, allow_redirects=True)

    #             with open(
    #                 f"{base_dir}{feat['properties']['OriginDate'].split('T')[0]}.zip", #location to save zip from copernicus 
    #                 "wb",
    #             ) as p:
    #                 print(feat['properties']['OriginDate'].split('T')[0])
    #                 p.write(file.content)
    #         except:
    #             print("problem with server")
else :
    print('no data found')