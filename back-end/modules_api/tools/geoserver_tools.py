import requests
import os
from requests.auth import HTTPBasicAuth

GEOSERVER_URL = "http://geoserver:8080/geoserver"
USERNAME = "test"
PASSWORD = "123"



def delete_workspace(workspace_name, recurse=True):
    """
    Deletes a workspace in GeoServer.

    Args:
        workspace_name (str): The name of the workspace to delete.
        recurse (bool): Whether to delete the workspace and all associated stores and layers (default is False).
    """
    delete_url = f"{GEOSERVER_URL}/rest/workspaces/{workspace_name}"
    if recurse:
        delete_url += "?recurse=true"
    
    response = requests.delete(delete_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 200:
        print(f"Workspace '{workspace_name}' deleted successfully.")
    elif response.status_code == 404:
        print(f"Workspace '{workspace_name}' not found.")
    else:
        print(f"Failed to delete workspace '{workspace_name}': {response.status_code} - {response.content.decode()}")


def publish_single_layer(workspace, tiff_file, var):

    create_store_url = f"{GEOSERVER_URL}/rest/workspaces/{workspace}/coveragestores"
    container_folder = f"/data/{workspace}/{var}"
    tiff_name = tiff_file.split('.')[0]

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
    response = requests.post(create_store_url, data=store_payload, headers={'Content-Type': 'text/xml'}, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 201:
        print(f"Store '{tiff_name}' created successfully.")
    elif response.status_code == 409:
        print(f"Store '{tiff_name}' already exists.")
    else:
        print(f"Failed to create store: {response.content}")

      
    # Step 2: Publish the layer
    publish_layer_url = f"{GEOSERVER_URL}/rest/workspaces/{workspace}/coveragestores/{tiff_name}/coverages"
    layer_payload = f"""
    <coverage>
    <name>{tiff_name}</name>
    <title>{tiff_name} Layer</title>
    <srs>EPSG:32629</srs>
    </coverage>
    """
    response = requests.post(publish_layer_url, data=layer_payload, headers={'Content-Type': 'text/xml'}, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 201:
        print(f"Store '{tiff_name}' created successfully.")
    elif response.status_code == 409:
        print(f"Store '{tiff_name}' already exists.")
    else:
        print(f"Failed to create store: {response.content}")

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
    """
    Create `indexer.properties` and `timeregex.properties` for an ImageMosaic in the specified path.

    Args:
        path (str): The directory where the files should be created.
    """
    indexer_content = """TimeAttribute=ingestion
Schema=*the_geom:Polygon,location:String,ingestion:java.util.Date
PropertyCollectors=TimestampFileNameExtractorSPI[timeregex](ingestion)
"""

    timeregex_content = r"([0-9]{4}-[0-9]{2}-[0-9]{2})"  # Matches dates in format YYYY-MM-DD

    indexer_path = os.path.join(path, "indexer.properties")
    timeregex_path = os.path.join(path, "timeregex.properties")

    try:
        # Create and write indexer.properties
        with open(indexer_path, "w") as indexer_file:
            indexer_file.write(indexer_content)
        os.chmod(indexer_path, 0o777)

        # Create and write timeregex.properties
        with open(timeregex_path, "w") as timeregex_file:
            timeregex_file.write(timeregex_content)
        os.chmod(timeregex_path, 0o777)

        print(f"Created 'indexer.properties' at {indexer_path}")
        print(f"Created 'timeregex.properties' at {timeregex_path}")

    except Exception as e:
        print(f"Failed to create indexer or timeregex file: {e}")



# if __name__ == '__main__':
#     delete_workspace()