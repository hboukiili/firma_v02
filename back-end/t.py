import os

folder = f"/app/Data/fao_output"
field_folder = f"{folder}/{id}/ndvi"
if not os.path.exists(field_folder):
    print('m in')
    os.makedirs(field_folder)       