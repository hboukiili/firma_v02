# -*- coding: utf-8 -*-

#from math import *
import sys
import math
import numpy as np
import datetime
from osgeo import gdal,osr,ogr
from osgeo.gdalconst import *
import tarfile
import os
import glob
import shutil

import config

"""def sentinel2_process (input_dir,output_dir):
	\"""
		Process a compressed Sentinel-2 file to extract it, correct it with sen2cor, calculate the ndvi, and finally merge all the granules in one image.

		:param input_dir: 	directory of the downloaded Sentinel-2 products
		:param output_dir: 	directory of extraction for products
	\"""	
	unzip(input_dir,output_dir)
	sen2cor(output_dir)"""


def unzip (input_dir, output_dir):
	"""
		Unzip the .zip files of the input directory in the output directory if the file hasn't been extracted before
		
		:param input_dir: 	input directory
		:param output_dir: 	output directory
		:return: 		none
	"""
	#unzip the downloaded satellite-2 images
	for element in os.listdir(input_dir):
		#get the name without '.zip'
		nomElement = '.'.join(os.path.basename(element).split('.')[:-1])
		#check if the element is zipped and doesn't have been extracted before
		if element.endswith('.zip') and not (os.path.exists(os.path.join(output_dir, nomElement+'.SAFE'))):
			zippedfile = os.path.join(input_dir, element)
			unzip='unzip %s -d %s'%(zippedfile, output_dir)
			os.system(unzip)


def sen2corSplit(repert, img_name, landsat_local):
	"""
		Pocess a Sentinel-2 image by spliting it in granules in order to avoid memory errors.
		
		:param repert: 		directory of the image
		:param img_name: 	name of the image
	
	"""

	#import the file L2A_Bashrc from the installation directory of sen2cor
	os.system(". /home/michel/sen2cor/L2A_Bashrc")
	#set the PATH
	os.environ["PATH"]="/home/michel/anaconda2/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

	img_out = img_name + "_satirr"

	ndvi_list=[]
	pat=os.path.join(repert,img_name)

	pat_satirr=os.path.join(repert,img_name+'_satirr')
	try :
		os.mkdir(pat_satirr)
	except Exception as e:
		print('Error %s',e)
		pass
		

	list_granules=glob.glob(os.path.join(pat,"GRANULE/*"))
	for granule in list_granules:
		granule_name=granule.split('/')
		granule_name=granule_name[len(granule_name)-1]
		print(granule_name)
		granule_dir=os.path.join(repert,granule_name)
		# create the granule directory
		try :
			os.mkdir(granule_dir)
			# copy auxiliariy repertories
			shutil.copytree(os.path.join(pat,"AUX_DATA"),os.path.join(granule_dir,"AUX_DATA"))
			shutil.copytree(os.path.join(pat,"DATASTRIP"),os.path.join(granule_dir,"DATASTRIP"))
			shutil.copytree(os.path.join(pat,"HTML"),os.path.join(granule_dir,"HTML"))
			shutil.copytree(os.path.join(pat,"rep_info"),os.path.join(granule_dir,"rep_info"))
			
			# copy 4 auxiliary files
			file_list=glob.glob(os.path.join(pat,"*.*"))
			for fn in file_list:
				shutil.copyfile(fn,fn.replace(img_name,granule_name))
			# create GRANULE directory
			os.mkdir(os.path.join(granule_dir,"GRANULE"))
			# copy one granule tree
			shutil.copytree(os.path.join(pat,"GRANULE",granule_name),os.path.join(granule_dir,"GRANULE",granule_name))
		except Exception as e:
			pass

		#check if the granule is authorized before processsing it
		for authorized in config.S2A_authorized :
			#if the granule is authorized
			if (os.path.basename(granule).split("_")[9].split("T")[1]) == authorized:
				# execute sen2cor
				name = os.path.join(repert,granule_name)
				new_name = name.replace("L1C","MSIL1C")
				os.system("mv "+name+" "+new_name)
				print ("L2A_Process "+new_name+" --resolution 10")
				os.system("L2A_Process "+new_name+" --resolution 10")

				sen2cor_dir=granule_dir.replace("OPER","USER")

				# compute NDVI from sen2cor_dir
				ndvi(sen2cor_dir, repert, landsat_local)

				# rajouter le nom du fichier NDVI à la liste
				ndvi_list.append("/media/SATIRR/data/" + str(os.path.basename(sen2corDir)).replace("_N02.01","_ndvi")) 

				# CLEAN: delete sen2cor_dir and granule_dir
				#shutil.rmtree(granule_dir)
				#shutil.rmtree(sen2cor_dir)

				# fin de la boucle, on fait le merge des ndvis avec gdal_merge


def ndvi(sen2corDir, rep, flocal):
	"""
		Calculate the ndvi of the granule in the given directory. The granule must have been processed with sen2cor before.

		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""
	
	#Set the PATH
	os.environ["PATH"]="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

	baseNameBand = os.path.basename(sen2corDir).replace("MSIL1C","L1C")

	nameBand4 = sen2corDir + "/GRANULE/"+ os.path.basename(sen2corDir) + "/IMG_DATA/R10m/" + baseNameBand.replace("_N02.01","_B04_10m.jp2")
	nameBand8 = sen2corDir + "/GRANULE/"+ os.path.basename(sen2corDir) + "/IMG_DATA/R10m/" + baseNameBand.replace("_N02.01","_B08_10m.jp2")
	nameBandCLD = sen2corDir + "/GRANULE/"+ os.path.basename(sen2corDir) + "/IMG_DATA/R60m/" + baseNameBand.replace("_N02.01","_CLD.tif")

	nameNdvi = "/media/SATIRR/data/output/" + baseNameBand.replace("_N02.01","_ndvi.TIF")

	#get the original images
	for element in os.listdir(rep):
		#Use sen2cor on every element extraced that hasn't been processed yet
		if element==baseNameBand.replace("S2A_USER_MSI_L2A","S2A_OPER_MSI_L1C"):
			nameBand4Original = rep +"/"+ element + "/GRANULE/" + element +"/IMG_DATA/" + element.replace("N02.01","B04.jp2")
			nameBand8Original = rep +"/"+ element + "/GRANULE/" + element +"/IMG_DATA/" + element.replace("N02.01","B08.jp2")

	#import the coordonates of the wanted images (only necessary with the old version of sen2cor)
	georef(nameBand4, nameBand4Original)
	georef(nameBand8, nameBand8Original)

	try :

		#Cloud Mask :

		repert = sen2corDir + "/GRANULE/"+ baseNameBand + "/QI_DATA/"
		gml_fn_cld = os.path.join(repert, baseNameBand.replace("S2A_USER_MSI_L2A_TL","S2A_OPER_MSK_CLOUDS").replace("N02.01","B00_MSIL1C.gml"))
		(gmlshortnamecld, extension) = os.path.splitext(gml_fn_cld)
		shp_fn_cld = os.path.join(repert, baseNameBand.replace("S2A_USER_MSI_L2A_TL","S2A_OPER_MSK_CLOUDS").replace("N02.01","B00_MSIL1C.shp"))
		(shpshortnamecld, extension) = os.path.splitext(shp_fn_cld)

		#convert the .GML cloud mask in shapefile with ogr2ogr

		commande ='ogr2ogr '+ gmlshortnamecld + '.shp ' + gml_fn_cld
		print("\n" + commande)
		os.system(commande)
		
		#rasterize the cloud mask
		
		burnvalue = 1
		
		commande='gdal_rasterize -l ' + os.path.basename(shpshortnamecld) +' -burn '+str(burnvalue) + ' ' + shp_fn_cld + ' ' + nameBandCLD
		print("\n" + commande)
		os.system(commande)
		

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

		fileBandCLD = gdal.Open(nameBandCLD)
		bandCLD = fileBandCLD.GetRasterBand(1)

		
		nb_slice=20
		ndvi=np.zeros([rows,cols], 'Float32')		
		jr=math.ceil(rows/nb_slice)
		
		for j in range(0,nb_slice):
			L4=band4.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
			L8=band8.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
			LCLD=bandCLD.ReadAsArray(0,int(j*jr),cols,int(min(jr,rows-jr*j)))
			emprise=(L4!=0)
			tt=(((np.float32(L8)-np.float32(L4))/((np.float32(L4)+np.float32(L8)+0.0000001))) * ((np.float32(LCLD)-1.)*-1.) * 100.)+100
			tt= tt + (np.float32(LCLD)*-100.)
			tt = tt * emprise
			ndvi[j*jr:min((j+1)*jr,rows),:]=tt
			print ("Slice "+str(j+1))
		print ('OK')
		driverOut=gdal.GetDriverByName("GTiff") 
		rasterOut=driverOut.Create(nameNdvi,cols,rows,bands)
		rasterOut.SetGeoTransform(fileBand4.GetGeoTransform())
		rasterOut.SetProjection(fileBand4.GetProjection())			
		bandOut=rasterOut.GetRasterBand(1)
		bandOut.WriteArray(ndvi)
		
		print ('Fini')
	except Exception as e:
		print('Error %s',e)
		pass

	# ajout du nom du fichier de sortie à la liste à des fichiers NDVI
	flocal=open(landsat_local, 'a')
	flocal.write(nameNdvi+'\n')
	flocal.close()


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

