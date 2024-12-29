import requests
import os

GEOSERVER_URL = "http://geoserver:8080/geoserver"
USERNAME = "test"
PASSWORD = "123"

def create_workspace(WORKSPACE):
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

def create_store(WORKSPACE, DATASTORE, DATA_DIR):
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


def publish_layer(WORKSPACE, DATASTORE, LAYER_NAME):
    
   # Step 1: Publish the layer
    publish_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/coveragestores/{DATASTORE}/coverages"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    publish_payload = {
        "coverage": {
            "name": LAYER_NAME,
            "title": LAYER_NAME,
            "enabled": True
        }
    }

    response = requests.post(publish_url, json=publish_payload, headers=headers, auth=(USERNAME, PASSWORD))
    if response.status_code == 201:
        print(f"Layer '{LAYER_NAME}' published successfully.")
    else:
        print(f"Failed to publish layer: {response.status_code}")
        print(f"Response: {response.content}")
        exit()
        return

def enable_time_dimension(WORKSPACE, LAYER_NAME):

    # Step 2: Enable the time dimension
    url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/coveragestores/{LAYER_NAME}/coverages/{LAYER_NAME}.json"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Prepare time dimension configuration as part of the layer metadata
    payload ={
                "coverage": {
                "metadata": {
                    "entry": [
                            {
                                "@key": "time",
                                "dimensionInfo": {
                                    "enabled": True,
                                    "presentation": "LIST",
                                    "units": "ISO8601",
                                    "defaultValue": "",
                                    "nearestMatchEnabled": True,
                                    "rawNearestMatchEnabled": True,
                                    "nearestFailBehavior": "IGNORE"
                                }
                            }
                        ]
                    }
                }
            }

    # Send PUT request to update the layer
    response = requests.put(url, json=payload, headers=headers, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        print(f"Time dimension enabled successfully for layer '{response.content}'.")
    else:
        print(f"Failed to configure time dimension: {response.status_code}")
        print(f"Response: {response.content}")

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
            os.chmod(indexer_path, 0o777)
            indexer_file.write(indexer_content)
        print(f"Created 'indexer.properties' at {indexer_path}")

        with open(timeregex_path, "w") as timeregex_file:
            os.chmod(timeregex_path, 0o777)
            timeregex_file.write(timeregex_content)
        print(f"Created 'timeregex.properties' at {timeregex_path}")
    except Exception as e:
        print(f"Failed to create indexer or timeregex file: {e}")