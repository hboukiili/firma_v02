import requests
import os
import rasterio
import numpy as np
from datetime import datetime


# url = "https://rest.isric.org/soilgrids/v2.0/image"
# params = {
#     "property": "ocd",
#     "depth": "0-5cm",
#     "bbox": "-17.1010,20.7744,-1.0201,35.9223",
#     "format": "image/tiff"
# }

# response = requests.get(url, params=params)

# print(response.status_code)
# with open("soil_map_morocco.tiff", "wb") as f:
#     f.write(response.content)

path		= "/app/tools/fao_test/fao_output"
folders	= os.listdir(path)

def extract_date(file_name):
    return datetime.strptime(file_name.split('.')[0], '%Y-%m-%d')

start_date = "2024-01-30"
end_date = "2024-04-01"

final_data = []
for folder in folders:
    min_values, max_values, mean_values = [], [], []
    var = f"{path}/{folder}"
    files = [f for f in os.listdir(var) if os.path.isfile(os.path.join(var, f))]

    files = sorted(files, key=extract_date)
    x, y = files.index(f"{start_date}.tif"), files.index(f"{end_date}.tif")
    files = files[x:y]
    for file in files:
        tif = f"{var}/{file}"
        with rasterio.open(tif) as src:
            
            data = src.read(1)
            mean, min, max = np.nanmean(data), np.nanmin(data), np.nanmax(data)
            min_values.append(min), mean_values.append(mean), max_values.append(max)
            break 
    
    final_data.append({
        folder : {
        'min' :  min_values,
        'max'  : max_values,
        'mean' : mean_values
        }
    })

# for i in final_data:
#     print(i) 
        
