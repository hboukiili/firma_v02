# This file is part PyTSEB, consisting of of high level pyTSEB scripting
# Copyright 2016 Hector Nieto and contributors listed in the README.md file.
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

from configparser import ConfigParser, NoOptionError
import itertools

from .PyTSEB import PyTSEB, PyTSEB2T, PyDTD, PydisTSEB
from osgeo import gdal
import numpy as np
import rasterio
from pyTSEB.meteo_utils import calc_vapor_pressure
import os


class ParserError(Exception):

    def __init__(self, parameter, expected_type):
        self.param = parameter
        self.type = expected_type

class MyConfigParser(ConfigParser):

    def __init__(self, top_section, *args, **kwargs):
        super().__init__(*args, inline_comment_prefixes=('#',), **kwargs)
        self.section = top_section

    def myget(self, option, **kwargs):
        return super().get(self.section, option, **kwargs)

    def getint(self, option, **kwargs):
        try:
            val = super().getint(self.section, option, **kwargs)
        except ValueError:
            raise ParserError(option, 'int')

        return val

    def getfloat(self, option, **kwargs):
        try:
            val = super().getfloat(self.section, option, **kwargs)
        except ValueError:
            raise ParserError(option, 'float')

        return val

    def has_option(self, option):
        return super().has_option(self.section, option)


class TSEBConfigFileInterface():

    SITE_DESCRIPTION = [
        'landcover',
        'lat',
        'lon',
        'alt',
        'stdlon',
        'z_T',
        'z_u',
        'z0_soil'
    ]

    VEGETATION_PROPERTIES = [
        'leaf_width',
        'alpha_PT',
        'x_LAD'
    ]

    SPECTRAL_PROPERTIES = [
        'emis_C',
        'emis_S',
        'rho_vis_C',
        'tau_vis_C',
        'rho_nir_C',
        'tau_nir_C',
        'rho_vis_S',
        'rho_nir_S'
    ]

    MODEL_FORMULATION = [
        'model',
        'resistance_form',
        'KN_b',
        'KN_c',
        'KN_C_dash',
        'G_form',
        'G_constant',
        'G_ratio',
        'G_amp',
        'G_phase',
        'G_shape',
        'calc_row',
        'row_az',
        'output_file',
        'correct_LST',
        'flux_LR_method',
        'water_stress'
    ]

    IMAGE_VARS = [
        'T_R1',
        'T_R0',
        'VZA',
        'LAI',
        'f_c',
        'f_g',
        'h_C',
        'w_C',
        'input_mask',
        'subset',
        'time',
        'DOY',
        'T_A1',
        'T_A0',
        'u',
        'ea',
        'S_dn',
        'L_dn',
        'p',
        'flux_LR',
        'flux_LR_ancillary',
        'S_dn_24',
        'SZA',
        'SAA',
    ]

    POINT_VARS = [
        'f_c',
        'f_g',
        'w_C'
    ]

    def __init__(self):

        self.params = {}
        self.ready = False

    @staticmethod
    def parse_input_config(input_file, **kwargs):
        ''' Parses the information contained in a configuration file into a dictionary'''

        parser = MyConfigParser('top')
        with open(input_file) as conf_file:
            conf_file = itertools.chain(('[top]',), conf_file)  # dummy section to please parser
            parser.read_file(conf_file)

        return parser

    @staticmethod
    def _parse_common_config(parser):
        """Parse all the stuff that's the same for image and point"""

        conf = {}

        conf['model'] = parser.myget('model')
        conf['output_file'] = parser.myget('output_file')

        conf['resistance_form'] = parser.getint('resistance_form', fallback=None)

        conf['water_stress'] = parser.getint('water_stress', fallback=False)
        if conf['water_stress']:
            conf['Rst_min'] = parser.getfloat('Rst_min', fallback=100)
            conf['R_ss'] = parser.getfloat('R_ss', fallback=500)

        conf['calc_row'] = parser.getint('calc_row', fallback=[0, 0])

        if conf['calc_row'] != [0, 0]:
            row_az = parser.getfloat('row_az')
            conf['calc_row'] = [1, row_az]

        g_form = parser.getint('G_form', fallback=1)
        if g_form == 0:
            g_constant = parser.getfloat('G_constant')
            conf['G_form'] = [[0], g_constant]
        elif g_form == 2:
            g_params = [parser.getfloat(p) for p in ('G_amp', 'G_phase', 'G_shape')]
            conf['G_form'] = [[2, *g_params], 12.0]
        else:
            g_ratio = parser.getfloat('G_ratio')
            conf['G_form'] = [[1], g_ratio]

        if conf['model'] == 'disTSEB':
            conf['flux_LR_method'] = parser.myget('flux_LR_method')
            conf['correct_LST'] = parser.getint('correct_LST')

        return conf

    @staticmethod
    def _parse_image_config(parser, conf):
        """Parse the image specific things"""

        # remaining in MODEL_FORMULATION
        conf.update({p: parser.myget(p) for p in ['KN_b', 'KN_c', 'KN_C_dash']})

        conf.update({p: parser.myget(p) for p in TSEBConfigFileInterface.SITE_DESCRIPTION})
        conf.update({p: parser.myget(p) for p in TSEBConfigFileInterface.VEGETATION_PROPERTIES})
        conf.update({p: parser.myget(p) for p in TSEBConfigFileInterface.SPECTRAL_PROPERTIES})

        img_vars = set(TSEBConfigFileInterface.IMAGE_VARS)
        if conf['model'] != 'DTD':
            img_vars -= set(['T_A0', 'T_R0'])
        if conf['model'] != 'disTSEB':
            img_vars -= set(['flux_LR', 'flux_LR_ancillary'])
        if not parser.has_option('subset'):
            img_vars.remove('subset')

        for p in img_vars:
            if p in ['S_dn_24', "SZA", "SAA"]:
                conf.update({p: parser.myget(p, fallback='')})
            else:
                conf.update({p: parser.myget(p)})

        return conf

    @staticmethod
    def _parse_point_config(parser, conf):
        """Parse the point specific things"""

        # remaining in MODEL_FORMULATION
        conf.update({p: parser.getfloat(p) for p in ['KN_b', 'KN_c', 'KN_C_dash']})

        conf.update({p: parser.getfloat(p) for p in TSEBConfigFileInterface.SITE_DESCRIPTION})
        conf.update({p: parser.getfloat(p) for p in TSEBConfigFileInterface.VEGETATION_PROPERTIES})
        conf.update({p: parser.getfloat(p) for p in TSEBConfigFileInterface.SPECTRAL_PROPERTIES})

        conf['input_file'] = parser.myget('input_file')
        conf.update({p: parser.getfloat(p) for p in TSEBConfigFileInterface.POINT_VARS})

        return conf

    def get_data(self, parser, is_image):
        '''Parses the parameters in a configuration file directly to TSEB variables for running
           TSEB'''

        conf = self._parse_common_config(parser)

        try:
            if is_image:
                conf = self._parse_image_config(parser, conf)
            else:
                conf = self._parse_point_config(parser, conf)
            self.ready = True
        except NoOptionError as e:
            print(f'Error: missing parameter {e.option}')
        except ParserError as e:
            print(f'Error: could not parse parameter {e.param} as type {e.type}')

        self.params = conf

    def run(self, is_image):

        if self.ready:
            if self.params['model'] == "TSEB_PT":
                model = PyTSEB(self.params)
            elif self.params['model'] == "TSEB_2T":
                model = PyTSEB2T(self.params)
            elif self.params['model'] == "DTD":
                model = PyDTD(self.params)
            elif self.params['model'] == "disTSEB":
                model = PydisTSEB(self.params)
            else:
                print("Unknown model: " + self.params['model'] + "!")
                return None
            if is_image:
                model.process_local_image()
            else:
                in_data, out_data = model.process_point_series_array()
                return in_data, out_data
        else:
            print("pyTSEB will not be run due to errors in the input data.")

    def checkSize(self, file_path):
        with rasterio.open(file_path) as dataset:
            # Get the dimensions from the first band
            size = dataset.read(1).astype('float64').shape
            Xsize, Ysize = size[0], size[1]
        return Xsize, Ysize 


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
        
        output_file="/tmp/fc.tif"

        with rasterio.open(output_file, 'w', **profile) as dst:
            dst.write(fc.astype(np.float32), 1)
        return output_file

    def TA_Calcul(self, path_ta):
        
        with rasterio.open(path_ta) as tif1:

            Ta = tif1.read(1).astype('float64')
            print(np.nanmean(Ta))
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


    # def fix_data(self, date, Bassin):

    #     data            = self.params

    #     lst             = f"/app/tools/sentinel_downloads/m2m_data/LST_CLOUD_FREE_Kelvin.tif"
    #     Ta              = f"/app/tools/sentinel_downloads/m2m_data/ta_2m_temperature.tif"
    #     # u_w             = f"/Data/2018/weather/{Bassin}/{date}/u_w/11.tif"
    #     # v_w             = f"/Data/2018/weather/{Bassin}/{date}/v_w/11.tif"
    #     # b1              = f"/Data/2018/MOD09GA/{Bassin}/b1/{date}.tif"
    #     # b2              = f"/Data/2018/MOD09GA/{Bassin}/b2/{date}.tif"
    #     # Lai             = f"/Data/2018/Lai/{Bassin}/{date}.tif"
    #     u                 = '/app/tools/sentinel_downloads/m2m_data/wind_speed_2m.tif'
    #     Ysize, Xsize    = self.checkSize(lst)

    #     # new_ta          = f"/tmp/{date}_Ta.tif"
    #     # new_u_w         = f"/tmp/{date}_u_w.tif"
    #     # new_v_w         = f"/tmp/{date}_v_w.tif"
    #     # new_b1          = f"/tmp/{date}_b1.tif"
    #     # new_b2          = f"/tmp/{date}_b2.tif"
    #     new_lai         = f"/app/tools/sentinel_downloads/m2m_data/LAI.tif"

    #     with rasterio.open(lst) as t, \
    #         rasterio.open(u) as t1:
            
    #         u_mean = np.nanmean(t1.read(1))
    #         target_crs      = t.meta['crs']

    #     gdal.Warp(Ta, Ta, width= Xsize  , height = Ysize , 
    #                 resampleAlg = "nearest"   ,dstSRS=target_crs)
    #     # gdal.Warp(new_u_w, u_w, width= Xsize  , height = Ysize, 
    #     #             resampleAlg = "nearest" , dstSRS=target_crs)
    #     # gdal.Warp(new_v_w, v_w, width= Xsize  , height = Ysize  , 
    #     #             resampleAlg = "nearest", dstSRS=target_crs)
    #     # gdal.Warp(new_b1, b1,  width= Xsize  , height = Ysize  ,
    #     #             resampleAlg = "nearest", dstSRS=target_crs)
    #     # gdal.Warp(new_b2, b2, width= Xsize  , height = Ysize  ,
    #     #             resampleAlg = "nearest" ,dstSRS=target_crs)
    #     # gdal.Warp(new_lai, Lai,  width= Xsize  , height = Ysize  ,
    #     #             resampleAlg = "nearest" , dstSRS=target_crs)       
    #     # new_fc      = self.calcul_fc(new_b1,new_b2)
    #     # u           = self.calcul_u(new_u_w,new_v_w)
    #     ea              = calc_vapor_pressure(self.TA_Calcul(Ta))
    #     data["T_R1"]    = lst
    #     data["LAI"]     = new_lai
    #     data["T_A1"]    = Ta
    #     data["f_c"]     = ''
    #     data["u"]       = u_mean
    #     data["ea"]      = ea
    #     self.params     = data
    #     print('hello')
        # data["output_file"] = f"/pyTSEB/{Bassin}/{date}"


    def fix_data(self, date, Bassin):
        data   = self.params

        # Define file paths
        lst_path = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/lst.tif"
        ta_path  = "/app/tools/sentinel_downloads/m2m_data/Tensift/product/t2m.tif"
        u_path   = '/app/tools/sentinel_downloads/m2m_data/Tensift/product/wind_speed_2m.tif'
        new_lai  = f"/app/tools/sentinel_downloads/m2m_data/Tensift/product/LAI.tif"

        # Extract reference spatial information from the LST file
        with rasterio.open(lst_path) as lst_ds:
            target_crs = lst_ds.crs
            bounds     = lst_ds.bounds
            width      = lst_ds.width
            height     = lst_ds.height

        # Get target dimensions via your checkSize function (if needed)
        # Ysize, Xsize = self.checkSize(lst_path)

        # Function to check CRS and bounds and warp if needed.
        def reproject_if_needed(src_path):
            with rasterio.open(src_path) as src_ds:
                src_crs    = src_ds.crs
                src_bounds = src_ds.bounds
            # Compare the source with the target LST values
            if src_crs != target_crs or src_bounds != bounds:
                # Create warp options using the reference properties
                warp_options = gdal.WarpOptions(
                    width=width,
                    height=height,
                    dstSRS=target_crs.to_wkt(),
                    outputBounds=(bounds.left, bounds.bottom, bounds.right, bounds.top),
                    resampleAlg="nearest"
                )
                # Overwrite the source file with the warped file
                gdal.Warp(src_path, src_path, options=warp_options)
                print(f"Reprojected {src_path} to match target CRS and bounds.")
            else:
                print(f"{src_path} already matches target CRS and bounds.")

        # Check and reproject each file as necessary
        # reproject_if_needed(ta_path)
        # reproject_if_needed(u_path)
        # reproject_if_needed(new_lai)

        # For example, read the wind speed and compute a mean value
        with rasterio.open(u_path) as u_ds:
            u_mean = np.nanmean(u_ds.read(1))

        ea = calc_vapor_pressure(self.TA_Calcul(ta_path))

        # Update the data dictionary with the new file paths and computed values
        data["T_R1"] = lst_path
        data["LAI"]  = new_lai
        data["T_A1"] = ta_path
        data["f_c"]  = new_lai  # Adjust this if f_c should be different
        data["u"]    = u_mean
        data["ea"]   = ea
        self.params = data
        print('Data fixing complete!')