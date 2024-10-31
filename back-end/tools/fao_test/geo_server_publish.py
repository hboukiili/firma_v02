import os
import requests
from requests.auth import HTTPBasicAuth

# GeoServer details
geoserver_url = "http://localhost:8080/geoserver"
username = "test"
password = "123"

def create_workspace(workspace_name, namespace_uri):
	# Workspace details
	geoserver_url_ = "http://localhost:8080/geoserver/rest/workspaces"

	# XML payload for creating a workspace
	workspace_payload = f"""
	<workspace>
	<name>{workspace_name}</name>
	<namespace>{namespace_uri}</namespace>
	</workspace>
	"""

	# Sending POST request to create the workspace
	response = requests.post(
		geoserver_url_,
		data=workspace_payload,
		headers={"Content-Type": "application/xml"},
		auth=HTTPBasicAuth(username, password)
	)

	# Checking the response status
	if response.status_code == 201:
		print(f"Workspace '{workspace_name}' created successfully.")
	else:
		print(f"Failed to create workspace. Status code: {response.status_code}")
		print(response.text)

# Path to the folder with TIFF files
path 		= "./fao_output"
folders		= os.listdir(path)

# Loop through all the TIFF files in the folder
for workspace in folders:
	tiff_folder = f"{path}/{workspace}"
	create_workspace(workspace, f"http://firma.com/{workspace}")
	for tiff_file in os.listdir(tiff_folder):

		if tiff_file.endswith(".tif"):
			tiff_name = os.path.splitext(tiff_file)[0]
			
			container_folder = f"/data/{workspace}"
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
			response = requests.post(publish_layer_url, data=layer_payload, headers={'Content-Type': 'text/xml'}, auth=HTTPBasicAuth(username, password))
		print(workspace, response.status_code)
print("All TIFFs published!")

