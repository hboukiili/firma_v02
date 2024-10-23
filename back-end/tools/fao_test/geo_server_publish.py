import os
import requests
from requests.auth import HTTPBasicAuth

# GeoServer details
geoserver_url = "http://localhost:8080/geoserver"
username = "test"
password = "123"
workspace = "ndvi"

# Path to the folder with TIFF files
tiff_folder = "./fao_output/DP"

# Loop through all the TIFF files in the folder
for tiff_file in os.listdir(tiff_folder):
    if tiff_file.endswith(".tif"):
        tiff_name = os.path.splitext(tiff_file)[0]
        
        container_folder = "/data/DP"
        # Step 1: Create the coverage store
        create_store_url = f"{geoserver_url}/rest/workspaces/{workspace}/coveragestores"
        store_payload = f"""
        <coverageStore>
          <name>{tiff_name}</name>
          <type>GeoTIFF</type>
          <workspace>{workspace}</workspace>
          <enabled>true</enabled>
          <url>file:{container_folder}/{tiff_file}</url>
          <description>Raster Data</description>
        </coverageStore>
        """
        requests.post(create_store_url, data=store_payload, headers={'Content-Type': 'text/xml'}, auth=HTTPBasicAuth(username, password))
        
        # Step 2: Publish the layer
        publish_layer_url = f"{geoserver_url}/rest/workspaces/{workspace}/coveragestores/{tiff_name}/coverages"
        layer_payload = f"""
        <coverage>
          <name>{tiff_name}</name>
          <title>{tiff_name} Layer</title>
          <srs>EPSG:32629</srs>
        </coverage>
        """
        requests.post(publish_layer_url, data=layer_payload, headers={'Content-Type': 'text/xml'}, auth=HTTPBasicAuth(username, password))

print("All TIFFs published!")
