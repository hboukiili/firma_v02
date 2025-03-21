from sentinelsat import SentinelAPI

import os
from datetime import datetime
from sentinelsat import SentinelAPI

# Connect to Sentinel API
api = SentinelAPI("hm.boukiili97@gmail.com", "Mas123456789@", "https://apihub.copernicus.eu/apihub")


# Connect to Sentinel API
# api = SentinelAPI(USERNAME, PASSWORD, URL)

# Define Area of Interest (AOI) as a bounding box (minx, miny, maxx, maxy)
aoi = (-7.680666, 31.66625, -7.679883, 31.666687)

# Define date range properly
specific_date = datetime.strptime("2025-02-19", "%Y-%m-%d")
date_range = (specific_date, datetime.strptime("2025-02-25", "%Y-%m-%d"))

# Search for Sentinel-2 images with <10% cloud cover
products = api.query(
    aoi,
    date=date_range,
    platformname="Sentinel-3",
    producttype="SL_2_LST___",
)

# Download the first available image
if products:
    api.download_all(products)
    print("Download complete!")
else:
    print("No images found for the given date and location.")