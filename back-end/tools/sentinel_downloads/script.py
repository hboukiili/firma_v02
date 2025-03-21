
import json
import requests
import sys
import time
import argparse
import datetime
import threading
import re

path = "./m2m_data/Tensift" # Fill a valid path to save the downloaded files
maxthreads = 5 # Threads count for downloads
sema = threading.Semaphore(value=maxthreads)
label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Customized label using date time
threads = []

import json

# Open and load the GeoJSON file
with open("/app/tools/shapeFile.geojson") as f:
    geojson_data = json.load(f)

geojson_polygons = []
for feature in geojson_data["features"]:
    if 'Tensift' == feature['properties']['Bassin']:
        Tensift = feature['geometry']['coordinates']
        break

# send http request
def sendRequest(url, data, apiKey = None):  
    pos = url.rfind('/') + 1
    endpoint = url[pos:]
    json_data = json.dumps(data)
    
    if apiKey == None:
        response = requests.post(url, json_data)
    else:
        headers = {'X-Auth-Token': apiKey}              
        response = requests.post(url, json_data, headers = headers)    
    
    try:
      httpStatusCode = response.status_code 
      if response == None:
          print("No output from service")
          sys.exit()
      output = json.loads(response.text)	
      if output['errorCode'] != None:
          print("Failed Request ID", output['requestId'])
          print(output['errorCode'], "-", output['errorMessage'])
          sys.exit()
      if  httpStatusCode == 404:
          print("404 Not Found")
          sys.exit()
      elif httpStatusCode == 401: 
          print("401 Unauthorized")
          sys.exit()
      elif httpStatusCode == 400:
          print("Error Code", httpStatusCode)
          sys.exit()
    except Exception as e: 
          response.close()
          pos=serviceUrl.find('api')
          print(f"Failed to parse request {endpoint} response. Re-check the input {json_data}. The input examples can be found at {url[:pos]}api/docs/reference/#{endpoint}\n")
          sys.exit()
    response.close()    
    print(f"Finished request {endpoint} with request ID {output['requestId']}\n")
    
    return output['data']

def downloadFile(url):
    sema.acquire()
    global path
    try:        
        response = requests.get(url, stream=True)
        disposition = response.headers['content-disposition']
        filename = re.findall("filename=(.+)", disposition)[0].strip("\"")
        print(f"Downloading {filename} ...\n")
        if path != "" and path[-1] != "/":
            filename = "/" + filename
        open(path + filename, 'wb').write(response.content)
        print(f"Downloaded {filename}\n")
        sema.release()
    except Exception as e:
        print(f"Failed to download from {url}. {e}. Will try to re-download.")
        sema.release()
        runDownload(threads, url)
    
def runDownload(threads, url):
    thread = threading.Thread(target=downloadFile, args=(url,))
    threads.append(thread)
    thread.start()

if __name__ == '__main__': 
    #NOTE :: Passing credentials over a command line arguement is not considered secure
    #        and is used only for the purpose of being example - credential parameters
    #        should be gathered in a more secure way for production usage
    #Define the command line arguements
    
    # user input    
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-u', '--username', required=True, help='ERS Username')
    # parser.add_argument('-t', '--token', required=True, help='ERS application token')
    
    # args = parser.parse_args()
    
    # username = args.username
    # token = args.token     
    username = "hboukili"
    token = "ksaWFMAspj8XKqBfJs33c_7ywIdCoakCSfSh8sq2a5oznMW9lSP65!rPb62LRm4r"  # Replace with your valid token
    print("\nRunning Scripts...\n")
    
    serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
    
    # login-token
    payload = {'username' : username, 'token' : token}
    
    apiKey = sendRequest(serviceUrl + "login-token", payload)
    
    print("API Key: " + apiKey + "\n")
    
    datasetName = "landsat_ot_c2_l2"
    
    spatialFilter = {
        "filterType": "mbr",
        "lowerLeft": {"longitude": -9.5, "latitude": 30.0},
        "upperRight": {"longitude": -7.0, "latitude": 32.5}
    }

    # spatialFilter = {
    #     "filterType": "geojson",
    #     "geoJson": geojson_data
    # }
    
    # spatialFilter = {
    # "filterType": "geojson",
    # "geoJson": {
    #     "type": "Polygon",  # ✅ Fix: Use uppercase "Polygon"
    #     "coordinates": [  # ✅ Fix: Enclose coordinates in an extra array
    #         [
    #             [-5.891916606916112, 35.654632448607],
    #             [-1.3204521040811983, 32.76517713786235],
    #             [-8.436832237738798, 27.80854656282048],
    #             [-10.77070592230649, 28.64634130335226],
    #             [-5.9261280692880405, 35.80644320300027],
    #             [-5.891916606916112, 35.654632448607]  # ✅ Close the polygon
    #         ]
    #         ]
    #     }
    # }


    # print(spatialFilter)
    start_date = '2024-08-01'
    end_date = '2024-08-16'
    temporalFilter = {'start' : start_date, 'end' : end_date}
    
    payload = {'datasetName' : datasetName,
                               'SpatialFilterGeoJson' : spatialFilter,
                               'temporalFilter' : temporalFilter}                     
    
    print("Searching datasets...\n")
    datasets = sendRequest(serviceUrl + "dataset-search", payload, apiKey)
    
    print("Found ", len(datasets), " datasets\n")
    # download datasets
    for dataset in datasets:
        # Because I've ran this before I know that I want GLS_ALL, I don't want to download anything I don't
        # want so we will skip any other datasets that might be found, logging it incase I want to look into
        # downloading that data in the future.
        if dataset['datasetAlias'] != datasetName:
            print("Found dataset " + dataset['collectionName'] + " but skipping it.\n")
            continue
            
    #     # I don't want to limit my results, but using the dataset-filters request, you can
    #     # find additional filters
        
        acquisitionFilter =  {'start' : start_date, 'end' : end_date}
            
        payload = {'datasetName' : dataset['datasetAlias'], 
                                 'maxResults' : 1000,
                                 'startingNumber' : 1, 
                                 'sceneFilter' : {
                                                  'spatialFilter' : spatialFilter,
                                                  'acquisitionFilter' : acquisitionFilter}}
        
    #     # Now I need to run a scene search to find data to download
        print("Searching scenes...\n\n")   
        
        scenes = sendRequest(serviceUrl + "scene-search", payload, apiKey)
        # Did we find anything?
        print(scenes)
        if scenes['recordsReturned'] > 0:
            # Aggregate a list of scene ids
            sceneIds = []
            for result in scenes['results']:
                # Add this scene to the list I would like to download
                sceneIds.append(result['entityId'])
            
            # Find the download options for these scenes
            # NOTE :: Remember the scene list cannot exceed 50,000 items!
            payload = {'datasetName' : dataset['datasetAlias'], 'entityIds' : sceneIds}
                                
            downloadOptions = sendRequest(serviceUrl + "download-options", payload, apiKey)
        
            # Aggregate a list of available products
            downloads = []
            for product in downloadOptions:
                    # Make sure the product is available for this scene
                    if product['available'] == True and 'LC08' in product['displayId']:
                        print(product['available'], product['displayId'])
                        downloads.append({'entityId' : product['entityId'],
                                           'productId' : product['id']})
            
            # Did we find products?
            if downloads:
                requestedDownloadsCount = len(downloads)
                # set a label for the download request
                label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Customized label using date time
                payload = {'downloads' : downloads,
                                             'label' : label}
                # Call the download to get the direct download urls
                requestResults = sendRequest(serviceUrl + "download-request", payload, apiKey)          
                              
                # PreparingDownloads has a valid link that can be used but data may not be immediately available
                # Call the download-retrieve method to get download that is available for immediate download
                if requestResults['preparingDownloads'] != None and len(requestResults['preparingDownloads']) > 0:
                    payload = {'label' : label}
                    moreDownloadUrls = sendRequest(serviceUrl + "download-retrieve", payload, apiKey)
                    
                    downloadIds = []  
                    
                    for download in moreDownloadUrls['available']:
                        if str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']:
                            downloadIds.append(download['downloadId'])
                            runDownload(threads, download['url'])
                        
                    for download in moreDownloadUrls['requested']:
                        if str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']:
                            downloadIds.append(download['downloadId'])
                            runDownload(threads, download['url'])
                     
                    # Didn't get all of the reuested downloads, call the download-retrieve method again probably after 30 seconds
                    while len(downloadIds) < (requestedDownloadsCount - len(requestResults['failed'])): 
                        preparingDownloads = requestedDownloadsCount - len(downloadIds) - len(requestResults['failed'])
                        print("\n", preparingDownloads, "downloads are not available. Waiting for 30 seconds.\n")
                        time.sleep(30)
                        print("Trying to retrieve data\n")
                        moreDownloadUrls = sendRequest(serviceUrl + "download-retrieve", payload, apiKey)
                        for download in moreDownloadUrls['available']:                            
                            if download['downloadId'] not in downloadIds and (str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']):
                                downloadIds.append(download['downloadId'])
                                runDownload(threads, download['url'])
                            
                else:
                    # Get all available downloads
                    for download in requestResults['availableDownloads']:
                        runDownload(threads, download['url'])
        else:
            print("Search found no results.\n")
    
    print("Downloading files... Please do not close the program\n")
    for thread in threads:
        thread.join()
            
    print("Complete Downloading")
                
    # Logout so the API Key cannot be used anymore
    endpoint = "logout"  
    if sendRequest(serviceUrl + endpoint, None, apiKey) == None:        
        print("Logged Out\n\n")
    else:
        print("Logout Failed\n\n") 