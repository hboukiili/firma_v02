#    copernicus_user = "hm.boukiili97@gmail.com"
#    copernicus_password = "Mas123456789@"

import pandas as pd
import requests
import os
import zipfile

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 🔹 Step 1: Get Authentication Token
def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    r = requests.post(
        "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        data=data,
    )
    r.raise_for_status()  
    return r.json()["access_token"]

# 🔹 Step 2: Create an authenticated session
def get_session():

    copernicus_user = "hm.boukiili97@gmail.com"
    copernicus_password = "Mas123456789@" 
    session = requests.Session()
    keycloak_token = get_keycloak(copernicus_user, copernicus_password)
    session.headers.update({"Authorization": f"Bearer {keycloak_token}"})
    return session

# 🔹 Step 3: Define AOI and Search Parameters
start_date = "2025-02-03"
end_date = "2025-02-04"
data_collection = "SENTINEL-3"
aoi = "POLYGON((-7.680666 31.66665, -7.679964 31.666687, -7.679883 31.666271, -7.680436 31.666276, -7.680554 31.666536, -7.680666 31.66665))"
# product_type = "SL_2_LST___" 
product_type = "SL_2_LST___"  

# Corrected Query
query_url = (
    f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
    f"$filter=Collection/Name eq '{data_collection}' and "
    # f"ProductType eq '{product_type}' and "  # Capital 'P' in ProductType
    f"OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and "
    f"ContentDate/Start gt {start_date}T00:00:00.000Z and "
    f"ContentDate/Start lt {end_date}T00:00:00.000Z"
)


response = requests.get(query_url)
response.raise_for_status()  

# Convert JSON response to DataFrame
result = response.json()["value"]
# print(len(result))
for i in result:
    if 'S3B_SL_2_LST' in i["Name"]:
        product_id = i["Id"]
        product_name = i["Name"]

print(f"Selected Product: {product_name} (ID: {product_id})")

# 🔹 Step 6: Download the Selected Product
def download_product(product_id, save_path):
    session = get_session()
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
    
    # Handle Redirects
    response = session.get(url, allow_redirects=False)
    while response.status_code in (301, 302, 303, 307):
        print(f"Redirecting to {response.headers['Location']}")
        url = response.headers["Location"]
        response = session.get(url, allow_redirects=False)

    # Save ZIP File
    with open(save_path, "wb") as file:
        print(f"Downloading {product_name}...")
        file.write(response.content)
        print(f"Saved to {save_path}.")

    # 🔹 Step 7: Extract ZIP
    folder = f"./test"
    with zipfile.ZipFile(save_path, "r") as zip_ref:
        zip_ref.extractall(folder)
        print("Extraction complete!")

# 🔹 Step 8: Start Download
save_path = "./sentinel3_LST.zip"
download_product(product_id, save_path)
