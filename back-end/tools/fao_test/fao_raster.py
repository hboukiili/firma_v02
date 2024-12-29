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

# self, Kcbini=0.15, Kcbmid=1.10, Kcbend=0.25, Lini=20,
#                  Ldev=50, Lmid=60, Lend=30, hini=0.010, hmax=0.9,
#                  thetaFC=0.250, thetaWP=0.100, theta0=0.1, Zrini=0.15,
#                  Zrmax=1.2, pbase=0.50, Ze=0.10, REW=8.0, CN2=70,
#                  comment='')

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


def plot_values_with_date_range(values, date_range, variable, output_path='./chart'):
    """
    Plots values against a date range and saves the plot as a PNG file.

    Parameters:
        values (list or iterable): A list of values to plot.
        start_date (str): The start date in the format 'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
        output_path (str): Path to save the output PNG file.

    Returns:
        None
    """
    # Plot values against the date range
    plt.figure(figsize=(15, 4))
    plt.plot(date_range, values, marker='o', linestyle='-', label='Values')

    # Formatting the plot
    plt.xlabel('Date')
    plt.ylabel(variable)
    plt.title(f'Canopy cover fraction')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the plot as PNG
    plt.savefig(f"{output_path}/{variable}.png", format='png')
    plt.close()

    print(f"Plot saved as {output_path}")


def extract_date(file_name):
    return datetime.strptime(file_name.split('.')[0], '%Y-%m-%d')


start_date  = "2024-01-15"
end_date    = "2024-05-30"
lat         = 31.66600208716224
long        = -7.678419088737144
date_range  = pd.date_range(start=start_date, end=end_date, freq='D')
index = date_range.strftime('%Y-%j')

def fao_test():

    Kcb, FC, E, Zr, Ks, Kcadj, ETcadj, T, DP, Irrig, Rain, Runoff, ETref = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

    ndvi_folder = "/app/tools/fao_test/fao_output/ndvi"
    files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
    files = sorted(files, key=extract_date)
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
    airr.addset('2024-015', '2024-148', ksc=0.7, imax=20)
    while i < NDVIS[0].shape[0]:  # Loop over rows
        x = 0
        while x < NDVIS[0].shape[1]:  # Loop over columns
            fc  = []
            kcb = []
            for ndvi in NDVIS:
                fc_mean     = float(1.33 * ndvi[i][x] - 0.20)
                kcb_mean    = float(1.64 * (ndvi[i][x] - 0.14))
                
                if fc_mean < 0:
                     fc_mean = 0
                
                if kcb_mean < 0:
                     kcb_mean = 0

                fc.append(fc_mean)
                kcb.append(kcb_mean)

            data = pd.DataFrame({
                    'fc': fc,
                    'Kcb': kcb,
                    'h' : h,
                }, index=index)

            upd = fao.Update(data)
            
            mdl = fao.Model('2024-015', '2024-151', par, wth, autoirr=airr, upd=upd)

            mdl.run()

            plot_values_with_date_range(mdl.odata.fc.values, date_range, 'fc')
            exit()

            for llk, value in mdl.odata['fc'].items():
                if llk not in FC:
                    FC[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                FC[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Kcb'].items():
                if llk not in Kcb:
                    Kcb[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Kcb[llk][i, x] = value  # Assign to the correct position in the 2D array
    
            for llk, value in mdl.odata['E'].items():
                if llk not in E:
                    E[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                E[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Zr'].items():
                if llk not in Zr:
                    Zr[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Zr[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Ks'].items():
                if llk not in Ks:
                    Ks[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Ks[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Kcadj'].items():
                if llk not in Kcadj:
                    Kcadj[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Kcadj[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['ETcadj'].items():
                if llk not in ETcadj:
                    ETcadj[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                ETcadj[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['T'].items():
                if llk not in T:
                    T[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                T[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['DP'].items():
                if llk not in DP:
                    DP[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                DP[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Irrig'].items():
                if llk not in Irrig:
                    Irrig[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Irrig[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Rain'].items():
                if llk not in Rain:
                    Rain[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Rain[llk][i, x] = value  # Assign to the correct position in the 2D array

            for llk, value in mdl.odata['Runoff'].items():
                if llk not in Runoff:
                    Runoff[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                Runoff[llk][i, x] = value  # Assign to the correct position in the 2D array
            for llk, value in mdl.odata['ETref'].items():
                if llk not in ETref:
                    ETref[llk] = np.full((NDVIS[0].shape[0], NDVIS[0].shape[1]), np.nan)
                ETref[llk][i, x] = value  # Assign to the correct position in the 2D array

            print("pixel x : ", x, " done")


            x = x + 1
        
        print("pixel i : ", i, " done")
        
        i = i + 1

    for date_str in FC:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/FC/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/FC"):
                os.makedirs("/app/tools/fao_test/fao_output/FC")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(FC[date_str], 1)  # Write the data to the first band

    for date_str in Kcb:
        
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Kcb/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Kcb"):
                os.makedirs("/app/tools/fao_test/fao_output/Kcb")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Kcb[date_str], 1)  # Write the data to the first band


    for date_str in E:
        parsed_date = datetime.strptime(date_str, '%Y-%j')

        date = parsed_date.strftime('%Y-%m-%d')

        output_file = f"/app/tools/fao_test/fao_output/E/{date}.tif"
        if not os.path.exists("/app/tools/fao_test/fao_output/E"):
            os.makedirs("/app/tools/fao_test/fao_output/E")
        with rasterio.open(output_file, "w", **meta) as dest:
            dest.write(E[date_str], 1)  # Write the data to the first band

    for date_str in Zr:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Zr/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Zr"):
                os.makedirs("/app/tools/fao_test/fao_output/Zr")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Zr[date_str], 1)  # Write the data to the first band

    for date_str in Ks:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Ks/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Ks"):
                os.makedirs("/app/tools/fao_test/fao_output/Ks")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Ks[date_str], 1)  # Write the data to the first band

    for date_str in Kcadj:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Kcadj/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Kcadj"):
                os.makedirs("/app/tools/fao_test/fao_output/Kcadj")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Kcadj[date_str], 1)  # Write the data to the first band

    for date_str in ETcadj:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/ETcadj/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/ETcadj"):
                os.makedirs("/app/tools/fao_test/fao_output/ETcadj")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(ETcadj[date_str], 1)  # Write the data to the first band

    for date_str in T:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/T/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/T"):
                os.makedirs("/app/tools/fao_test/fao_output/T")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(T[date_str], 1)  # Write the data to the first band

    for date_str in DP:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/DP/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/DP"):
                os.makedirs("/app/tools/fao_test/fao_output/DP")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(DP[date_str], 1)  # Write the data to the first band
    
    for date_str in Irrig:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Irrig/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Irrig"):
                os.makedirs("/app/tools/fao_test/fao_output/Irrig")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Irrig[date_str], 1)  # Write the data to the first band

    for date_str in Rain:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Rain/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Rain"):
                os.makedirs("/app/tools/fao_test/fao_output/Rain")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Rain[date_str], 1)  # Write the data to the first band

    for date_str in Runoff:
            parsed_date = datetime.strptime(date_str, '%Y-%j')

            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/Runoff/{date}.tif"
            if not os.path.exists("/app/tools/fao_test/fao_output/Runoff"):
                os.makedirs("/app/tools/fao_test/fao_output/Runoff")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(Runoff[date_str], 1)  # Write the data to the first band

    for date_str in ETref:
            parsed_date = datetime.strptime(date_str, '%Y-%j')
            date = parsed_date.strftime('%Y-%m-%d')

            output_file = f"/app/tools/fao_test/fao_output/ETref/{date}.tif"
            
            if not os.path.exists("/app/tools/fao_test/fao_output/ETref"):
                os.makedirs("/app/tools/fao_test/fao_output/ETref")
            with rasterio.open(output_file, "w", **meta) as dest:
                dest.write(ETref[date_str], 1)  # Write the data to the first band


fao_test()