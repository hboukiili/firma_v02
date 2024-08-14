import requests

url = "https://rest.isric.org/soilgrids/v2.0/image"
params = {
    "property": "ocd",
    "depth": "0-5cm",
    "bbox": "-17.1010,20.7744,-1.0201,35.9223",
    "format": "image/tiff"
}

response = requests.get(url, params=params)

print(response.status_code)
# with open("soil_map_morocco.tiff", "wb") as f:
#     f.write(response.content)