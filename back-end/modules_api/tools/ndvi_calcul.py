from osgeo import ogr
import os,sys
import logging
from xml.dom import minidom
import glob
from osgeo import gdal
import numpy as np
import math
import shutil
import scipy.ndimage as ndimage



ValuesListDict_high_probability = {'bords':[0],'nuages' : [8,9,10], 'ombres' : [3], 'neige' : [11], 'eau' : [6]}

gdal.UseExceptions()

def read_tif(nameNdvi):

	ndvi = gdal.Open(nameNdvi)
	band1 = ndvi.GetRasterBand(1)

	# Get raster dimensions
	rows = ndvi.RasterYSize
	cols = ndvi.RasterXSize

	# Number of slices (as in your NDVI writing step)
	nb_slices = 10
	jr = math.ceil(rows / nb_slices)

	# Loop through slices to check values
	for j in range(0, nb_slices):
		print("Slice " + str(j + 1))
		
		# Read the slice from the TIFF
		slice_data = band1.ReadAsArray(0, int(j * jr), cols, int(min(jr, rows - jr * j)))
		
		# print("Min NDVI:", slice_data.min())
		# print("Max NDVI:", slice_data.max())
		# print("Mean NDVI:", slice_data.mean())


def decodeMasqueSen2cor(msq):
	masque = np.zeros_like(msq)

	for maskType in ValuesListDict_high_probability.keys():
		for val in ValuesListDict_high_probability[maskType]:
			masque = np.where(msq==val, 1, masque)

	return masque

Cloud_mask_sen2cor = True

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



def S2_ndvi(fname_L2A,dir_NDVI,flocal='./flocal'):
	"""
		Calculate the ndvi of the granule in the given directory. The granule must have been processed with sen2cor before.

		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""
	
	# ajout du nom du fichier de sortie à la liste à des fichiers NDVI
	flocal=open(flocal, 'a')
	#Set the PATH
	#os.environ["PATH"]="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
	
	subdir = fname_L2A + '/' + [d for d in os.listdir(fname_L2A) if os.path.isdir(os.path.join(fname_L2A, d))][0] + '/GRANULE'
	subdir = subdir + '/' + [d for d in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, d))][0]
	print(os.path.join(subdir, "R10m"))
	# # bug si les fichiers n'existent pas, attention au [0]
	nameBand4 = glob.glob(os.path.join(subdir, "IMG_DATA","R10m")+os.sep+"*B04*.jp2")[0]
	nameBand8 =  glob.glob(os.path.join(subdir , "IMG_DATA","R10m")+os.sep+"*B08*.jp2")[0]
	nameBandCLD = nameBand8[:-11] + "CLD.tif"
	fname=fname_L2A.split(os.sep)[-1]
	nameNdvi = fname+'_ndvi.tif'
	nameNdvi = os.path.join(dir_NDVI, nameNdvi)
	# read_tif(nameNdvi)
	# exit()
	# print(fname_L2A,nameNdvi)
	# print(nameBand4)
	# print(nameBand8)
	if os.path.exists(nameBand4) is True and  os.path.exists(nameBand8) is True :
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
			# if Cloud_mask_L1C is True:
		
			# 	gml_fn_cld = glob.glob(os.path.join(subdir , "QI_DATA")+os.sep+"MSK_CLOUDS_B00.gml")[0]
			# 	(gmlshortnamecld, extension) = os.path.splitext(gml_fn_cld)
			# 	shp_fn_cld = gml_fn_cld.replace("MSK_CLOUDS_B00.gml","MSK_CLOUDS_B00.shp")
			# 	(shpshortnamecld, extension) = os.path.splitext(shp_fn_cld)
		
			# 	#convert the .GML cloud mask in shapefile with ogr2ogr
		
			# 	commande ='ogr2ogr '+ gmlshortnamecld + '.shp ' + gml_fn_cld
			# 	print("\n" + commande)
			# 	os.system(commande)
				
			# 	#rasterize the cloud mask
				
			# 	burnvalue = 1
			# 	shp_attrib='maskType'
			# 	#shp_attrib=shpshortnamecld
			# 	#os.system('gdal_rasterize -a ICE_TYPE -where \"ICE_TYPE=\'Open Water\'\" -burn 2 -l ' + shapefileshortname +' -tr 1000 -1000 ' +  shapefile + ' ' + outraster) 
	
			# 	commande="/usr/local/bin/gdal_rasterize "+' -te '+str(xmin)+' '+str(ymax)+' '+str(xmax)+' '+str(ymin)+' -tr '+str(xres)+' '+str(yres)+' -a '+shp_attrib+' -where \"'+'maskType'+'=\''+'OPAQUE'+'\'\" -burn '+str(burnvalue)+' -l ' + os.path.basename(gmlshortnamecld) + ' "' + gmlshortnamecld + '.shp' + '" "' + nameBandCLD+'"'
			# 	print("\n" + commande)
			# 	os.system(commande)			
			# 	commande="/usr/local/bin/gdal_rasterize "+' -a '+shp_attrib+' -where \"'+'maskType'+'=\''+'CIRRUS'+'\'\" -b 1 -burn '+str(burnvalue)+' -l ' + os.path.basename(gmlshortnamecld) + ' "' + gmlshortnamecld + '.shp' + '" "' + nameBandCLD+'"'
			# 	print("\n" + commande)
			# 	os.system(commande)	
			# 	#commande='gdal_rasterize -l ' + os.path.basename(shpshortnamecld) +' -burn '+str(burnvalue) + ' ' + shp_fn_cld + ' ' + nameBandCLD
			# 	#print("\n" + commande)
			# 	#os.system(commande)
				
			# 	fileBandCLD = gdal.Open(nameBandCLD)
			# 	bandCLD = fileBandCLD.GetRasterBand(1)
			# 	LCLD=bandCLD.ReadAsArray()
			# 	fileBandCLD = None

			# Cloud Mask from Sen2cor
			if Cloud_mask_sen2cor is True:
				nameCloud = glob.glob(os.path.join(subdir , "IMG_DATA","R20m")+os.sep+"*SCL*.jp2")[0]
				print("cloud file : %s"%nameCloud)
				
				msq,nb_col,nb_lig = lire_masque_sen2cor(nameCloud)
				LCLD=decodeMasqueSen2cor(msq)
			
	
			#Open the bands 4, 8 and the cloud raster
			fileBand4 = gdal.Open(nameBand4)
			# print(fileBand4.GetProjection())
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
			rasterOut=driverOut.Create(nameNdvi,cols,rows,bands, gdal.GDT_Float32)
			rasterOut.SetGeoTransform(fileBand4.GetGeoTransform())
			rasterOut.SetProjection(fileBand4.GetProjection())			
			bandOut=rasterOut.GetRasterBand(1)
			for j in range(0, nb_slice):
				print("Slice " + str(j + 1))
				
				# Read slices of the Red and NIR bands
				L4 = band4.ReadAsArray(0, int(j * jr), cols, int(min(jr, rows - jr * j)))
				L8 = band8.ReadAsArray(0, int(j * jr), cols, int(min(jr, rows - jr * j)))
				
				# Read the cloud mask slice
				LCLD1 = LCLD[int(j * jr):int(min(rows, jr * j + jr)), 0:cols]
				
				# Define the emprise mask where L4 is not zero
				emprise = (L4 != 0)
				
				# Calculate NDVI, ensuring no division by zero
				tt = (np.float32(L8) - np.float32(L4)) / (np.float32(L8) + np.float32(L4) + 0.0000001) * ((np.float32(LCLD1) - 1.) * -1.)
				
				# Apply emprise mask to exclude no-data pixels (where L4 is 0)
				tt = tt * emprise
				
				# print("Min NDVI:", tt.min())
				# print("Max NDVI:", tt.max())
				# print("Mean NDVI:", tt.mean())

				# Write array to output TIFF here

				bandOut.WriteArray(np.float32(tt), 0, int(j * jr))
							
			# del driverOut
			
			print ('OK')

			#bandOut.WriteArray(ndvi)
			# flocal.write(nameNdvi+'\n')

			fileBand4=None
			fileBand8=None
			# shutil.rmtree(fname_L2A)
			print ('Fini')
			
		except Exception as e:
			print('Error ndvi %s',e)
			pass

	flocal.close()			



# base_directory = "/app/tools/aquacrop_test/sentinel_data/zip_folders"
# subdirectories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
# for i in subdirectories:
# 	print(i)
# 	i = "2024-01-16"
# 	directory = "/app/tools/aquacrop_test/sentinel_data/zip_folders/" + i 
# 	S2_ndvi(directory, "/app/tools/aquacrop_test/sentinel_data/ndvi", "/app/tools/aquacrop_test/sentinel_data/flocal")
# 	break