import os
import requests

# GeoServer connection details
GEOSERVER_URL = "http://geoserver:8080/geoserver"
USERNAME = "test"
PASSWORD = "123"

# Configuration
WORKSPACE = "test_workspace"
DATASTORE = "test_store"
DATA_DIR = "/data/119/ndvi"
CRS = "EPSG:32629"  # Change to your CRS (e.g., EPSG:32629 for UTM Zone 29N)

def create_workspace():
    url = f"{GEOSERVER_URL}/rest/workspaces"
    headers = {"Content-Type": "application/json"}
    data = {"workspace": {"name": WORKSPACE}}
    response = requests.post(url, json=data, headers=headers, auth=(USERNAME, PASSWORD))
    if response.status_code == 201:
        print(f"Workspace '{WORKSPACE}' created successfully.")
    elif response.status_code == 409:
        print(f"Workspace '{WORKSPACE}' already exists.")
    else:
        print(f"Failed to create workspace: {response.content}")

def create_store():
    url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/coveragestores"
    headers = {"Content-Type": "application/json"}
    data = {
        "coverageStore": {
            "name": DATASTORE,
            "type": "ImageMosaic",
            "enabled": True,
            "workspace": WORKSPACE,
            "url": f"file://{DATA_DIR}"
        }
    }
    response = requests.post(url, json=data, headers=headers, auth=(USERNAME, PASSWORD))
    if response.status_code == 201:
        print(f"Store '{DATASTORE}' created successfully.")
    elif response.status_code == 409:
        print(f"Store '{DATASTORE}' already exists.")
    else:
        print(f"Failed to create store: {response.content}")


def publish_layer(LAYER_NAME):
    LAYER_NAME = DATA_DIR.split('/')[-1]
    url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/coveragestores/{DATASTORE}/coverages"
    headers = {
        "Content-Type": "application/json",  # Specify the request payload type
        "Accept": "application/json"  # Optionally, specify the response format
    }
    data = {
        "coverage": {
            "name": LAYER_NAME,
            "title": LAYER_NAME,
            "enabled": True,
            "metadata": {
                "time": {
                    "enabled": True,  # Enable time dimension
                    "default": "minmax" ,
                    "presentation": "LIST"
                }
            }
        }
    }
    
    print(f"Publishing layer '{LAYER_NAME}'...")
    
    response = requests.post(url, json=data, headers=headers, auth=(USERNAME, PASSWORD))
    
    if response.status_code == 201:
        print(f"Layer '{LAYER_NAME}' published successfully.")
    else:
        print(f"Failed to publish layer: {response.status_code}")
        print(f"Response: {response.content}")
        if response.status_code == 404:
            print("Check if the workspace and datastore exist.")
        elif response.status_code == 401:
            print("Authentication failed. Check your username and password.")
        elif response.status_code == 400:
            print("Bad request. Ensure all metadata and configurations are correct.")


def create_indexer_and_timeregex(path):
    
    indexer_content = """TimeAttribute=time
Schema=*the_geom:Polygon,location:String,time:java.util.Date
PropertyCollectors=TimestampFileNameExtractorSPI[timeregex](time)
"""

    timeregex_content = r"\d{4}-\d{2}-\d{2}"
    indexer_path = os.path.join(path, "indexer.properties")
    timeregex_path = os.path.join(path, "timeregex.properties")

    try:
        with open(indexer_path, "w") as indexer_file:
            indexer_file.write(indexer_content)
        print(f"Created 'indexer.properties' at {indexer_path}")

        with open(timeregex_path, "w") as timeregex_file:
            timeregex_file.write(timeregex_content)
        print(f"Created 'timeregex.properties' at {timeregex_path}")
    except Exception as e:
        print(f"Failed to create indexer or timeregex file: {e}")

if __name__ == "__main__":

    create_workspace()
    create_store()
    create_indexer_and_timeregex()
    publish_layer()
