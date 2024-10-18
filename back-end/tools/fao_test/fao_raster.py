from fao_test import Open_meteo
import os
import rasterio
import numpy as np
import pyfao56 as fao
import pandas as pd
from datetime import datetime
# [
#   [
#     -7.678321344603916,
#     31.66580238055144
#   ],
#   [
#     -7.677650988631882,
#     31.66569305230466
#   ],
#   [
#     -7.6775747205875575,
#     31.664825254781007
#   ],
#   [
#     -7.678229020127901,
#     31.6648901690497
#   ],
#   [
#     -7.678333386926454,
#     31.665795547539773
#   ]
# ]

start_date  = "2024-01-15"
end_date    = "2024-05-30"
lat         = 31.66600208716224
long        = -7.678419088737144
date_range  = pd.date_range(start=start_date, end=end_date, freq='D')
index = date_range.strftime('%Y-%j')

def fao_test():

    Kcb, FC, E, Zr, Ks, Kcadj, ETcadj, T, DP, Irrig, Rain, Runoff = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

    ndvi_folder = "/app/tools/fao_test/interpolated_ndvi"
    files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
    NDVIS = []
    raster_crs = None

    for file in files:
        with rasterio.open(f"{ndvi_folder}/{file}") as src:
            
            if raster_crs == None:
                meta = src.meta.copy()
                raster_crs = src.crs
                transform = src.transform
    
            NDVIS.append(src.read(1))
    h = [np.nan] * len(NDVIS)
    i = 0
    weather_data = Open_meteo(start_date, end_date, lat, long)
    par = fao.Parameters()
    wth = fao.Weather(weather_data, index)
    airr = fao.AutoIrrigate()
    airr.addset('2024-015', '2024-145', ksc=0.7)
    while i < NDVIS[0].shape[0]:  # Loop over rows
        x = 0
        while x < NDVIS[0].shape[1]:  # Loop over columns
            fc  = []
            kcb = []
            for ndvi in NDVIS:

                fc.append(float(1.33 * ndvi[i][x] - 0.20))
                kcb.append(float(1.64 * (ndvi[i][x] - 0.14)))

                # print("ndvi : ", ndvi[i][x], "fc : ", float(1.33 * ndvi[i][x] - 0.20), " kcb ", float(1.64 * (ndvi[i][x] - 0.14)))

            data = pd.DataFrame({
                    'fc': fc,
                    'Kcb': kcb,
                    'h' : h,
                }, index=index)

            upd = fao.Update(data)
            
            mdl = fao.Model('2024-015', '2024-151', par, wth, autoirr=airr, upd=upd)

            mdl.run()

            print(mdl.odata)
            exit()

            # for llk, value in mdl.odata['fc'].items():
            #     if llk not in FC:
            #         FC[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     FC[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['E'].items():
            #     if llk not in E:
            #         E[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     E[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['Zr'].items():
            #     if llk not in Zr:
            #         Zr[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     Zr[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['Ks'].items():
            #     if llk not in Ks:
            #         Ks[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     Ks[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['Kcadj'].items():
            #     if llk not in Kcadj:
            #         Kcadj[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     Kcadj[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['ETcadj'].items():
            #     if llk not in ETcadj:
            #         ETcadj[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     ETcadj[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['T'].items():
            #     if llk not in T:
            #         T[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     T[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['DP'].items():
            #     if llk not in DP:
            #         DP[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     DP[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['Irrig'].items():
            #     if llk not in Irrig:
            #         Irrig[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     Irrig[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['Rain'].items():
            #     if llk not in Rain:
            #         Rain[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     Rain[llk][i, x] = value  # Assign to the correct position in the 2D array

            # for llk, value in mdl.odata['Runoff'].items():
            #     if llk not in Runoff:
            #         Runoff[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
            #     Runoff[llk][i, x] = value  # Assign to the correct position in the 2D array

            print("pixel x : ", x, " done")


            x = x + 1
        
        print("pixel i : ", i, " done")
        
        i = i + 1

    # for date_str in FC:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/FC/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/FC"):
    #             os.makedirs("/app/tools/fao_test/fao_output/FC")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(FC[date_str], 1)  # Write the data to the first band

    # for date_str in E:
    #     parsed_date = datetime.strptime(date_str, '%Y-%j')

    #     date = parsed_date.strftime('%Y-%m-%d')

    #     output_file = f"/app/tools/fao_test/fao_output/E/{date}.tif"
    #     if not os.path.exists("/app/tools/fao_test/fao_output/E"):
    #         os.makedirs("/app/tools/fao_test/fao_output/E")
    #     with rasterio.open(output_file, "w", **meta) as dest:
    #         dest.write(E[date_str], 1)  # Write the data to the first band

    # for date_str in Zr:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/Zr/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/Zr"):
    #             os.makedirs("/app/tools/fao_test/fao_output/Zr")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(Zr[date_str], 1)  # Write the data to the first band

    # for date_str in Ks:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/Ks/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/Ks"):
    #             os.makedirs("/app/tools/fao_test/fao_output/Ks")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(Ks[date_str], 1)  # Write the data to the first band

    # for date_str in Kcadj:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/Kcadj/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/Kcadj"):
    #             os.makedirs("/app/tools/fao_test/fao_output/Kcadj")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(Kcadj[date_str], 1)  # Write the data to the first band

    # for date_str in ETcadj:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/ETcadj/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/ETcadj"):
    #             os.makedirs("/app/tools/fao_test/fao_output/ETcadj")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(ETcadj[date_str], 1)  # Write the data to the first band

    # for date_str in T:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/T/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/T"):
    #             os.makedirs("/app/tools/fao_test/fao_output/T")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(T[date_str], 1)  # Write the data to the first band

    # for date_str in DP:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/DP/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/DP"):
    #             os.makedirs("/app/tools/fao_test/fao_output/DP")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(DP[date_str], 1)  # Write the data to the first band
    
    # for date_str in Irrig:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/Irrig/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/Irrig"):
    #             os.makedirs("/app/tools/fao_test/fao_output/Irrig")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(Irrig[date_str], 1)  # Write the data to the first band

    # for date_str in Rain:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/Rain/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/Rain"):
    #             os.makedirs("/app/tools/fao_test/fao_output/Rain")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(Rain[date_str], 1)  # Write the data to the first band

    # for date_str in Runoff:
    #         parsed_date = datetime.strptime(date_str, '%Y-%j')

    #         date = parsed_date.strftime('%Y-%m-%d')

    #         output_file = f"/app/tools/fao_test/fao_output/Runoff/{date}.tif"
    #         if not os.path.exists("/app/tools/fao_test/fao_output/Runoff"):
    #             os.makedirs("/app/tools/fao_test/fao_output/Runoff")
    #         with rasterio.open(output_file, "w", **meta) as dest:
    #             dest.write(Runoff[date_str], 1)  # Write the data to the first band


fao_test()