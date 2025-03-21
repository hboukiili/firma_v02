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


delete_workspace('test')