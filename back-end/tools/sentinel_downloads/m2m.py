import json
import requests
import sys
import time
import datetime
import threading
import re

# ---------------------------
# Configuration
# ---------------------------
path = "./m2m_data"  # Directory to save downloads
maxthreads = 5  # Number of concurrent downloads
sema = threading.Semaphore(value=maxthreads)
threads = []

username = "hboukili"
token = "ksaWFMAspj8XKqBfJs33c_7ywIdCoakCSfSh8sq2a5oznMW9lSP65!rPb62LRm4r"  # Replace with your valid token

serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
datasetName = "landsat_ot_c2_l2"

spatialFilter = {
    'filterType': "mbr",
    'lowerLeft': {"longitude": -7.68, "latitude": 31.66},
    'upperRight': {"longitude": -7.67, "latitude": 31.67}
}

temporalFilter = {'start': '2024-01-01', 'end': '2024-01-30'}


# ---------------------------
# Helper: sendRequest
# ---------------------------
def sendRequest(url, data, apiKey=None):
    """ Sends an HTTP request and handles errors """
    json_data = json.dumps(data)

    headers = {'X-Auth-Token': apiKey} if apiKey else {}
    response = requests.post(url, data=json_data, headers=headers)

    try:
        output = response.json()
        if response.status_code >= 400 or output.get('errorCode'):
            print(f"❌ Error in request {url}: {output.get('errorMessage', 'Unknown error')}")
            sys.exit()
        print(f"✅ Finished request {url} with request ID {output.get('requestId')}")
        return output['data']
    except Exception as e:
        print(f"❌ Failed to parse response for {url}. Error: {e}")
        sys.exit()


# ---------------------------
# Helper: Download File
# ---------------------------
def downloadFile(url):
    sema.acquire()
    try:
        response = requests.get(url, stream=True)
        disposition = response.headers.get('content-disposition', '')
        filename = re.findall("filename=(.+)", disposition)[0].strip("\"") if disposition else "downloaded_file.tar"
        full_path = f"{path}/{filename}"

        print(f"📥 Downloading {filename} ...")
        with open(full_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded {filename} to {full_path}\n")
    except Exception as e:
        print(f"❌ Failed to download {url}. Error: {e}")
    finally:
        sema.release()


def runDownload(threads, url):
    """ Creates a thread for downloading files """
    thread = threading.Thread(target=downloadFile, args=(url,))
    threads.append(thread)
    thread.start()


# ---------------------------
# Main Workflow
# ---------------------------
if __name__ == '__main__':
    print("\n🚀 Running Script...\n")

    # --- 1. Log In using the Application Token ---
    login_payload = {'username': username, 'token': token}
    apiKey = sendRequest(serviceUrl + "login-token", login_payload)
    print("🔑 API Key Acquired\n")

    # --- 2. Validate Dataset Name ---
    dataset_payload = {'datasetName': datasetName}
    dataset_info = sendRequest(serviceUrl + "dataset-search", dataset_payload, apiKey)

    if not dataset_info:
        print(f"❌ Dataset '{datasetName}' is invalid.")
        sys.exit()

    # --- 3. Search for Scenes ---
    print("🔍 Searching for available scenes...\n")

    sceneFilter = {
        "spatialFilter": spatialFilter,
        "acquisitionFilter": temporalFilter
    }

    search_payload = {
        "datasetName": datasetName,
        "maxResults": 5,  # Adjust the number of results if needed
        "startingNumber": 1,
        "sceneFilter": sceneFilter
    }

    search_data = sendRequest(serviceUrl + "scene-search", search_payload, apiKey)
    scenes = search_data.get("results", [])

    if not scenes:
        print("❌ No scenes found for the selected area and date range.")
        sys.exit()

    print("📌 Found Scenes:")
    for scene in scenes:
        print(f" - Entity ID: {scene['entityId']}, Display ID: {scene['displayId']}")

    # --- 4. Get Download Options ---
    chosen_scene = scenes[0]['entityId']  # Select the first scene
    print(f"\n📝 Checking download options for scene: {chosen_scene}")

    download_options_payload = {"datasetName": datasetName, "entityIds": [chosen_scene]}
    download_options = sendRequest(serviceUrl + "download-options", download_options_payload, apiKey)

    available_products = [product for product in download_options if product.get("available")]

    if not available_products:
        print("❌ No available download options for this scene.")
        sys.exit()

    # --- 5. Place Order for Scene Download ---
    print(f"\n📦 Placing order for scene: {chosen_scene}")

    order_payload = {
        "datasetName": datasetName,
        "downloads": [{"entityId": chosen_scene, "productId": available_products[0]["id"]}],
        "label": label
    }

    order_data = sendRequest(serviceUrl + "download-request", order_payload, apiKey)

    # --- 6. Retrieve Download URLs ---
    print("\n📡 Retrieving download links...")

    download_retrieve_payload = {"label": label}
    download_links = sendRequest(serviceUrl + "download-retrieve", download_retrieve_payload, apiKey)

    available_links = download_links.get("available", [])
    if available_links:
        for link in available_links:
            runDownload(threads, link["url"])
    else:
        print("⚠️ No download URLs available yet. Try checking later.")

    # Wait for all downloads to finish
    for thread in threads:
        thread.join()

    # --- 7. Logout ---
    sendRequest(serviceUrl + "logout", None, apiKey)
    print("✅ Logged out successfully.\n")
