# This file is part PyTSEB, consisting of of high level pyTSEB scripting
# Copyright 2018 Radoslaw Guzinski and contributors listed in the README.md file.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from re import match

from pyMETRIC.PyMETRIC import PyMETRIC
from osgeo import gdal
import numpy as np
import rasterio
from pyTSEB.meteo_utils import calc_vapor_pressure

class METRICConfigFileInterface():

    def __init__(self):

        self.params = {}
        self.ready = False

        temp_params = {'model': 'METRIC', 'use_METRIC_resistance': 1, 'G_form': 0,
                       'water_stress': False}
        temp_model = PyMETRIC(temp_params)
        self.input_vars = temp_model._get_input_structure().keys()

    def parse_input_config(self, input_file, is_image=True):
        ''' Parses the information contained in a configuration file into a dictionary'''

        if not is_image:
            print("Point time-series interface is not implemented for ESVEP!")
            return None

        # Read contents of the configuration file
        config_data = dict()
        try:
            with open(input_file, 'r') as fid:
                for line in fid:
                    if match('\s', line):  # skip empty line
                        continue
                    elif match('#', line):  # skip comment line
                        continue
                    elif '=' in line:
                        # Remove comments in case they exist
                        line = line.split('#')[0].rstrip(' \r\n')
                        field, value = line.split('=')
                        config_data[field] = value
        except IOError:
            print('Error reading ' + input_file + ' file')

        return config_data

    def get_data(self, config_data, is_image):
        '''Parses the parameters in a configuration file directly to METRIC variables for running
           METRIC'''

        if not is_image:
            print("Point time-series interface is not implemented for METRIC!")
            return None

        try:
            for var_name in self.input_vars:
                try:
                    self.params[var_name] = str(config_data[var_name]).strip('"')
                except KeyError:
                    pass

            self.params['model'] = config_data['model']

            if 'calc_row' not in config_data or int(config_data['calc_row']) == 0:
                self.params['calc_row'] = [0, 0]
            else:
                self.params['calc_row'] = [
                    1,
                    float(config_data['row_az'])]
            
            if 'water_stress' not in config_data:
                self.params['water_stress'] = False
            else:
                self.params['water_stress'] = bool(int(config_data['water_stress']))

            if int(config_data['G_form']) == 0:
                self.params['G_form'] = [[0], float(config_data['G_constant'])]
            elif int(config_data['G_form']) == 1:
                self.params['G_form'] = [[1], float(config_data['G_ratio'])]
            elif int(config_data['G_form']) == 2:
                self.params['G_form'] = [[2,
                                         float(config_data['G_amp']),
                                         float(config_data['G_phase']),
                                         float(config_data['G_shape'])],
                                         12.0]
            elif int(config_data['G_form']) == 4:
                self.params['G_form'] = [[4],
                                         (float(config_data['G_tall']), 
                                          float(config_data['G_short']))]
            elif int(config_data['G_form']) == 5:
                self.params['G_form'] = [[5], None]

            self.params['output_file'] = config_data['output_file']

            self.ready = True

        except KeyError as e:
            print('Error: missing parameter '+str(e)+' in the input data.')
        except ValueError as e:
            print('Error: '+str(e))

    def run(self, is_image):

        if not is_image:
            print("Point time-series interface is not implemented for METRIC!")
            return None

        if self.ready:
            if self.params['model'] == "pyMETRIC":
                model = PyMETRIC(self.params)
            else:
                print("Unknown model: " + self.params['model'] + "!")
                return None
            model.process_local_image()
            
        else:
            print("pyMETRIC will not be run due to errors in the input data.")


    def checkSize(self, file_path):
        
        with rasterio.open(file_path) as dataset:
            
            size = dataset.read(1).astype('float64').shape
            # crs = dataset.crs
            # bounds= dataset.bounds
            Xsize, Ysize = size[0], size[1]
        #     transform= dataset.transform
        # file_name = file_path.split("/")[-1].split(".")[0]

        # print(f"{file_name}:  Xsize = {Xsize} ,  Ysize = {Ysize}")  
        # print(f"{crs}")
        # print(transform)
        # print(f"{bounds}")
        # print("------------------------------------------------------------------")
        
        return Xsize , Ysize

    def calcul_fc(self, path_b1,path_b2):

            
        with rasterio.open(path_b1) as b1, \
            rasterio.open(path_b2) as b2:

            nir = b2.read(1).astype('float32')
            red = b1.read(1).astype('float32')
            

            np.seterr(divide='ignore', invalid='ignore')
            ndvi = (nir - red) / (nir + red)
            ndvi[np.isinf(ndvi)] = np.nan
            ndvi[np.isnan(ndvi)] = np.nan

            NDVIv = 0.95  # NDVI for complete vegetation cover
            NDVIs = 0.05  # NDVI for bare soil or non-vegetated areas

            fc = (ndvi - NDVIs) / (NDVIv - NDVIs)

            profile = b1.profile.copy()
        
        output_file ="/tmp/fc.tif"
        ndvi_file = "/tmp/NDVI.tif"

        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(fc.astype(np.float32), 1)

        with rasterio.open(ndvi_file, 'w', **profile) as dst2:
            dst2.write(ndvi.astype(np.float32), 1)

        return output_file, ndvi_file 
    
    def TA_Calcul(self, path_ta):
        
        with rasterio.open(path_ta) as tif1:

            Ta = tif1.read(1).astype('float64')

            Ta[Ta == 9999] = np.nan

            return np.nanmean(Ta)
    
    def calcul_u(self, path_u,path_v):
        
        with rasterio.open(path_u) as u, \
            rasterio.open(path_v) as v:

            u_w = u.read(1).astype('float64')
            v_w = v.read(1).astype('float64')
            
            u_w[u_w == 9999] = np.nan
            v_w[v_w == 9999] = np.nan
            
            u_mean = np.nanmean(u_w)
            v_mean = np.nanmean(v_w)

            wind_speed = np.sqrt(u_mean**2 + v_mean**2)

            return wind_speed
    
    def fix_data(self, date, Bassin):
        
        
        data = self.params
        
        lst =  f"/Data/2018/MOD11A1/{Bassin}/LST_Day_1km/{date}.tif"
        Ta =   f"/Data/2018/weather/{Bassin}/{date}/t2m/11.tif"
        u_w =  f"/Data/2018/weather/{Bassin}/{date}/u_w/11.tif"
        v_w =  f"/Data/2018/weather/{Bassin}/{date}/v_w/11.tif"
        b1 =   f"/Data/2018/MOD09GA/{Bassin}/b1/{date}.tif"
        b2 =   f"/Data/2018/MOD09GA/{Bassin}/b2/{date}.tif"
        Lai = f"/Data/2018/Lai/{Bassin}/{date}.tif"

        Ysize, Xsize = self.checkSize(lst)

        new_ta= f"/tmp/{date}_Ta.tif"
        new_u_w= f"/tmp/{date}_u_w.tif"
        new_v_w= f"/tmp/{date}_v_w.tif"
        new_b1= f"/tmp/{date}_b1.tif"
        new_b2= f"/tmp/{date}_b2.tif"
        new_lai= f"/tmp/{date}_lai.tif"
        target_crs = 'EPSG:4326'
        
        gdal.Warp(new_ta, Ta, width= Xsize  , height = Ysize , 
                resampleAlg = "nearest"   ,dstSRS=target_crs)
        gdal.Warp(new_u_w, u_w, width= Xsize  , height = Ysize, 
                    resampleAlg = "nearest" , dstSRS=target_crs)
        gdal.Warp(new_v_w, v_w, width= Xsize  , height = Ysize  , 
                    resampleAlg = "nearest", dstSRS=target_crs)
        gdal.Warp(new_b1, b1,  width= Xsize  , height = Ysize  ,
                    resampleAlg = "nearest", dstSRS=target_crs)
        gdal.Warp(new_b2, b2, width= Xsize  , height = Ysize  ,
                    resampleAlg = "nearest" ,dstSRS=target_crs)
        gdal.Warp(new_lai, Lai,  width= Xsize  , height = Ysize  ,
                    resampleAlg = "nearest" , dstSRS=target_crs)       
        
        fc, ndvi = self.calcul_fc(new_b1,new_b2)

        u = self.calcul_u(new_u_w,new_v_w)

        ea = calc_vapor_pressure(self.TA_Calcul(new_ta))

        
        data["T_R1"] = lst
        data["LAI"]  = new_lai
        data["T_A1"] = new_ta   
        data["f_c"]  = fc
        data["u"] = u
        data["ea"] = ea
        data["VI"] = ndvi
        data["output_file"] = f"/pyMETRIC/{Bassin}/{date}.vrt"
        self.params = data
