# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 13:48:36 2017


Download and Process Sentinel2 images 

Download code from https://github.com/olivierhagolle/Sentinel-download
Process is done with Sen2cor with Anaconda in python 2.7 while this code is python3.3 based :/

"""

from osgeo import ogr
import os,sys
import logging
from xml.dom import minidom
import glob
from osgeo import gdal
import numpy as np
import math
import scipy.ndimage as ndimage
import shutil

gdal.UseExceptions()

from S2_config import *

#import shapely
#from shapely.wkt import loads 
#from shapely.geometry.base import geom_from_wkt
"""
S2_authorized=["31TCJ","31TDJ","31TCH","31TDH","31TCG","30TYM","31TBG","29SPR","29SNR","29RNQ","29RPQ","32SNE","32SPE","30TYP","30TXP"]

downloader="aria2"
url_search="https://scihub.copernicus.eu/apihub/search?q="
account="michel"
passwd="michel123"
write_dir='.'
sentinel="S2"
no_download=True

path_to_sen2cor='/home/michel/sen2cor'
path_to_anaconda2 = '/home/michel/anaconda2'

Cloud_mask_L1C = False
Cloud_mask_sen2cor = True

#ValuesListDict_medium_probability = {'bords':[0],'nuages' : [8,9,10], 'ombres' : [3], 'neige' : [11], 'eau' : [6]}
#ValuesListDict_high_probability = {'bords':[0],'nuages' : [9,10], 'ombres' : [3], 'neige' : [11], 'eau' : [6]}
ValuesListDict_high_probability = {'bords':[0],'nuages' : [9,10], 'ombres' : [3]}
"""

"""
def decodeMasqueSen2cor(msq):
	masques = {}

	for maskType in ValuesListDict_high_probability.keys():
		masques[maskType] = np.zeros_like(msq)
		for val in ValuesListDict_high_probability[maskType]:
			masques[maskType] = np.where(msq==val, 1, masques[maskType])

	return masques
"""

def decodeMasqueSen2cor(msq):
	masque = np.zeros_like(msq)

	for maskType in ValuesListDict_high_probability.keys():
		for val in ValuesListDict_high_probability[maskType]:
			masque = np.where(msq==val, 1, masque)

	return masque
	
def lire_masque_sen2cor(nom_masque) :

	ds_masque=gdal.Open(nom_masque)
	nb_col_20m=ds_masque.RasterXSize
	nb_lig_20m=ds_masque.RasterYSize

	nb_col_10m=ds_masque.RasterXSize
	nb_lig_10m=ds_masque.RasterYSize

	msq = ds_masque.GetRasterBand(1).ReadAsArray()
	msq = ndimage.zoom(msq,2,order=0)
	ds_masque = None
	
	return msq,nb_col_10m,nb_lig_10m
				
#============ Code copied from http://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings ====

def GetExtent(gt,cols,rows):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
        yarr.reverse()
    return ext

def georef(L2A_img,L1C_img):
	input_img=gdal.Open(L2A_img)
	L1C_img=gdal.Open(L1C_img)
	geo = L1C_img.GetGeoTransform()
	input_img.SetGeoTransform(geo)
	PJ=L1C_img.GetProjection()
	input_img.SetProjection(PJ)
	return
	
def S2_ndvi(fname_L2A,dir_NDVI,flocal):
	"""
		Calculate the ndvi of the granule in the given directory. The granule must have been processed with sen2cor before.

		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""
	
	# ajout du nom du fichier de sortie à la liste à des fichiers NDVI
	flocal=open(flocal, 'a')
	#Set the PATH
	#os.environ["PATH"]="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
	
	subdir=glob.glob(fname_L2A+os.sep+'GRANULE'+os.sep+'*')[0]
	print(subdir)

	# bug si les fichiers n'existent pas, attention au [0]
	nameBand4 = glob.glob(os.path.join(subdir , "IMG_DATA","R10m")+os.sep+"*B04*.jp2")[0]
	nameBand8 =  glob.glob(os.path.join(subdir , "IMG_DATA","R10m")+os.sep+"*B08*.jp2")[0]
	nameBandCLD = nameBand8[:-11] + "CLD.tif"

	fname=fname_L2A.split(os.sep)[-1]
	ladate = fname[45:53]
	nameNdvi = fname[38:44]+'_'+ladate[0:4]+'.'+ladate[4:6]+'.'+ladate[6:8]+'_ndvi.tif'
	nameNdvi = os.path.join(dir_NDVI, nameNdvi)
	
	print(fname_L2A,nameNdvi)
	print(nameBand4)
	print(nameBand8)
	print(nameBandCLD)
	
	if os.path.exists(nameNdvi) is False and os.path.exists(nameBand4) is True and  os.path.exists(nameBand8) is True :
		print("calcul")
	
		try :


			ref_img = gdal.Open(nameBand4)
			cols=ref_img.RasterXSize
			rows=ref_img.RasterYSize
			GT=ref_img.GetGeoTransform()
			xmin=str(GT[0])
			ymin=str(GT[3])
			xmax=str(GT[0]+GT[1]*cols)
			ymax=str(GT[3]+GT[5]*rows)
			xres=GT[1]
			yres=-GT[5]	
			ref_img=None
			
			# Cloud Mask  from L1C
			if Cloud_mask_L1C is True:
		
				gml_fn_cld = glob.glob(os.path.join(subdir , "QI_DATA")+os.sep+"MSK_CLOUDS_B00.gml")[0]
				(gmlshortnamecld, extension) = os.path.splitext(gml_fn_cld)
				shp_fn_cld = gml_fn_cld.replace("MSK_CLOUDS_B00.gml","MSK_CLOUDS_B00.shp")
				(shpshortnamecld, extension) = os.path.splitext(shp_fn_cld)
		
				#convert the .GML cloud mask in shapefile with ogr2ogr
		
				commande ='ogr2ogr '+ gmlshortnamecld + '.shp ' + gml_fn_cld
				print("\n" + commande)
				os.system(commande)
				
				#rasterize the cloud mask
				
				burnvalue = 1
				shp_attrib='maskType'
				#shp_attrib=shpshortnamecld
				#os.system('gdal_rasterize -a ICE_TYPE -where \"ICE_TYPE=\'Open Water\'\" -burn 2 -l ' + shapefileshortname +' -tr 1000 -1000 ' +  shapefile + ' ' + outraster) 
	
				commande="/usr/local/bin/gdal_rasterize "+' -te '+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+' -tr '+str(xres)+' '+str(yres)+' -a '+shp_attrib+' -where \"'+'maskType'+'=\''+'OPAQUE'+'\'\" -burn '+str(burnvalue)+' -l ' + os.path.basename(gmlshortnamecld) + ' "' + gmlshortnamecld + '.shp' + '" "' + nameBandCLD+'"'
				print("\n" + commande)
				os.system(commande)			
				commande="/usr/local/bin/gdal_rasterize "+' -a '+shp_attrib+' -where \"'+'maskType'+'=\''+'CIRRUS'+'\'\" -b 1 -burn '+str(burnvalue)+' -l ' + os.path.basename(gmlshortnamecld) + ' "' + gmlshortnamecld + '.shp' + '" "' + nameBandCLD+'"'
				print("\n" + commande)
				os.system(commande)	
				#commande='gdal_rasterize -l ' + os.path.basename(shpshortnamecld) +' -burn '+str(burnvalue) + ' ' + shp_fn_cld + ' ' + nameBandCLD
				#print("\n" + commande)
				#os.system(commande)
				
				fileBandCLD = gdal.Open(nameBandCLD)
				bandCLD = fileBandCLD.GetRasterBand(1)
				LCLD=bandCLD.ReadAsArray()
				fileBandCLD = None

			# Cloud Mask from Sen2cor
			if Cloud_mask_sen2cor is True:
				nameCloud = glob.glob(os.path.join(subdir , "IMG_DATA","R20m")+os.sep+"*SCL*.jp2")[0]
				print("cloud file : %s"%nameCloud)
				
				msq,nb_col,nb_lig = lire_masque_sen2cor(nameCloud)
				LCLD=decodeMasqueSen2cor(msq)
			
	
			#Open the bands 4, 8 and the cloud raster
			fileBand4 = gdal.Open(nameBand4)
			print(fileBand4.GetProjection())
			cols = fileBand4.RasterXSize
			rows = fileBand4.RasterYSize
			bands =  fileBand4.RasterCount # normalement 1
			driver = fileBand4.GetDriver()
			gt=fileBand4.GetGeoTransform()
			ext=GetExtent(gt,cols,rows)
			band4 = fileBand4.GetRasterBand(1)
		
			fileBand8 = gdal.Open(nameBand8)
			band8 = fileBand8.GetRasterBand(1)
	
			nb_slice=10
			#ndvi=np.zeros([rows,cols], 'Float32')		
			jr=math.ceil(rows/nb_slice)

			driverOut=gdal.GetDriverByName("GTiff") 
			rasterOut=driverOut.Create(nameNdvi,cols,rows,bands)
			rasterOut.SetGeoTransform(fileBand4.GetGeoTransform())
			rasterOut.SetProjection(fileBand4.GetProjection())			
			bandOut=rasterOut.GetRasterBand(1)
			
			for j in range(0,nb_slice):
				print ("Slice "+str(j+1))
				L4=band4.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
				L8=band8.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
				LCLD1=LCLD[int(j*jr):int(min(rows,jr*j+jr)),0:cols]
				emprise=(L4!=0)
				tt=(((np.float32(L8)-np.float32(L4))/((np.float32(L4)+np.float32(L8)+0.0000001))) * ((np.float32(LCLD1)-1.)*-1.) * 100.)+100
				tt= tt + (np.float32(LCLD1)*-100.)
				tt = tt * emprise
				
				bandOut.WriteArray(np.byte(tt),0,int(j*jr))
				
				#ndvi[j*jr:min((j+1)*jr,rows),:]=tt
			del driverOut
			print ('OK')

			#bandOut.WriteArray(ndvi)
			flocal.write(nameNdvi+'\n')

			fileBand4=None
			fileBand8=None
			shutil.rmtree(fname_L2A)
			print ('Fini')
			
		except Exception as e:
			print('Error ndvi %s',e)
			pass

	flocal.close()			

def S2_ndvi_theia(fname_L2A,dir_NDVI,flocal):
	"""
		Calculate the ndvi of the granule in the given directory. The granule must have been processed with sen2cor before.

		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""
	
	# ajout du nom du fichier de sortie à la liste à des fichiers NDVI
	flocal=open(flocal, 'a')
	#Set the PATH
	os.environ["PATH"]="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
	
	subdir=fname_L2A
	print(subdir)

	# bug si les fichiers n'existent pas, attention au [0]
	nameBand4 = glob.glob(subdir+os.sep+"*_FRE_B4*.tif")[0]
	nameBand8 = glob.glob(subdir+os.sep+"*_FRE_B8*.tif")[0]
	nameBandCLD = glob.glob(subdir+os.sep+"MASKS"+os.sep+"*_CLM_R1.tif")[0]

	fname=fname_L2A.split(os.sep)[-1]
	ladate = fname.split('_')[1].split('-')[0]
	tile=fname.split('_')[3]	
	nameNdvi = tile+'_'+ladate[0:4]+'.'+ladate[4:6]+'.'+ladate[6:8]+'_ndvi.tif'
	nameNdvi = os.path.join(dir_NDVI, nameNdvi)
	
	print(fname_L2A,nameNdvi)
	print(nameBand4)
	print(nameBand8)
	print(nameBandCLD)
	
	if os.path.exists(nameNdvi) is False and os.path.exists(nameBand4) is True and  os.path.exists(nameBand8) is True :
		print("calcul")
	
		try :


			ref_img = gdal.Open(nameBand4)
			cols=ref_img.RasterXSize
			rows=ref_img.RasterYSize
			GT=ref_img.GetGeoTransform()
			xmin=str(GT[0])
			ymin=str(GT[3])
			xmax=str(GT[0]+GT[1]*cols)
			ymax=str(GT[3]+GT[5]*rows)
			xres=GT[1]
			yres=-GT[5]	
			ref_img=None

			# Cloud Mask from Sen2cor
			if Cloud_mask_sen2cor is True:
				nameCloud = glob.glob(subdir+os.sep+"MASKS"+os.sep+"*_CLM_R1.tif")[0]
				print("cloud file : %s"%nameCloud)
				ff = gdal.Open(nameCloud)
				msq = ff.GetRasterBand(1).ReadAsArray()
				LCLD = msq > 0
				ff=None
			
	
			#Open the bands 4, 8 and the cloud raster
			fileBand4 = gdal.Open(nameBand4)
			cols = fileBand4.RasterXSize
			rows = fileBand4.RasterYSize
			bands =  fileBand4.RasterCount # normalement 1
			driver = fileBand4.GetDriver()
			gt=fileBand4.GetGeoTransform()
			ext=GetExtent(gt,cols,rows)
			band4 = fileBand4.GetRasterBand(1)
		
			fileBand8 = gdal.Open(nameBand8)
			band8 = fileBand8.GetRasterBand(1)
	
			nb_slice=10
			#ndvi=np.zeros([rows,cols], 'Float32')		
			jr=math.ceil(rows/nb_slice)

			driverOut=gdal.GetDriverByName("GTiff") 
			rasterOut=driverOut.Create(nameNdvi,cols,rows,bands)
			rasterOut.SetGeoTransform(fileBand4.GetGeoTransform())
			rasterOut.SetProjection(fileBand4.GetProjection())			
			bandOut=rasterOut.GetRasterBand(1)
			
			for j in range(0,nb_slice):
				print ("Slice "+str(j+1))
				L4=band4.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
				L8=band8.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
				LCLD1=LCLD[int(j*jr):int(min(rows,jr*j+jr)),0:cols]
				emprise=(L4!=0)
				tt=(((np.float32(L8)-np.float32(L4))/((np.float32(L4)+np.float32(L8)+0.0000001))) * ((np.float32(LCLD1)-1.)*-1.) * 100.)+100
				tt= tt + (np.float32(LCLD1)*-100.)
				tt = tt * emprise
				
				bandOut.WriteArray(tt,0,int(j*jr))
				
				#ndvi[j*jr:min((j+1)*jr,rows),:]=tt
			print ('OK')

			#bandOut.WriteArray(ndvi)
			flocal.write(nameNdvi+'\n')

			fileBand4=None
			fileBand8=None
			rasterOut=None
			shutil.rmtree(fname_L2A)
			print ('Fini')
			
		except Exception as e:
			print('Error ndvi %s',e)
			pass

	flocal.close()		
	
if __name__ == "__main__":
	
#	S2_lat, S2_lon=S2_tile_centroid(S2_authorized)
#	
#	for i in range(len(S2_authorized)):
#		tile=S2_authorized[i]
#		lat=S2_lat[i]
#		lon=S2_lon[i]
#		print("-----> DOWNLOAD %s <-----"%tile)
#		#S2_download(lat,lon)
#
#		list_zip=glob.glob(os.path.join(write_dir,'inputs',"*%s*.zip"%tile))
#		for fname in list_zip:
#			S2_Process(fname)
	
#	list_L2A = glob.glob(os.path.join(write_dir,'inputs',"S2A_MSIL2A*SAFE"))
#	print(list_L2A)
#	dir_NDVI=os.path.join(write_dir,'outputs')
#	flocal=os.path.join(dir_NDVI,'flocal.txt')	
#	for L2A in list_L2A:
#		print(L2A)
#		fname=S2_ndvi(L2A,dir_NDVI,flocal)

	list_L2A = glob.glob(os.path.join(write_dir,'inputs',"SENTINEL2*_D_*"))
	print(list_L2A)
	dir_NDVI=os.path.join(write_dir,'outputs')
	flocal=os.path.join(dir_NDVI,'flocal.txt')	
	for L2A in list_L2A:
		print(L2A)
		fname=S2_ndvi_theia(L2A,dir_NDVI,flocal)	
