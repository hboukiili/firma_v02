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

def lire_masque_sen2cor(nom_masque):
    # Open the Sen2Cor mask file (assumed at 20 m resolution)
    ds_masque = gdal.Open(nom_masque)
    nb_col_20m = ds_masque.RasterXSize
    nb_lig_20m = ds_masque.RasterYSize

    # Read the mask data from the first raster band
    msq = ds_masque.GetRasterBand(1).ReadAsArray()
    
    # Upsample the mask by a factor of 2 (from 20 m to 10 m) using nearest neighbor interpolation
    msq_10m = ndimage.zoom(msq, 2, order=0)
    
    # Close the dataset
    ds_masque = None

    # Update the dimensions to reflect the upsampled 10 m resolution
    nb_col_10m = nb_col_20m * 2
    nb_lig_10m = nb_lig_20m * 2

    return msq_10m, nb_col_10m, nb_lig_10m

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



def S2_ndvi(fname_L2A,dir_NDVI,specefic_date,flocal='./flocal'):
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
	nameNdvi = f'{specefic_date}_ndvi.tif'
	nameNdvi = os.path.join(dir_NDVI, nameNdvi)

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

			for j in range(nb_slice):
				print("Processing Slice " + str(j + 1))

				# Read slices of the Red (B4) and NIR (B8) bands
				L4 = band4.ReadAsArray(0, int(j * jr), cols, int(min(jr, rows - jr * j)))
				L8 = band8.ReadAsArray(0, int(j * jr), cols, int(min(jr, rows - jr * j)))

				# Read the binary cloud mask slice (LCLD1: 1 = cloud/problematic, 0 = clear)
				LCLD1 = LCLD[int(j * jr):int(min(rows, jr * j + jr)), 0:cols]

				# Define valid data mask: only pixels where L4 is nonzero
				valid_mask = (L4 != 0)

				# Convert L4 and L8 to reflectance by dividing by 10,000
				L4 = L4.astype(np.float32) / 10000.0
				L8 = L8.astype(np.float32) / 10000.0

				# Calculate NDVI using the standard formula, adding a small constant to avoid division by zero
				ndvi = (L8 - L4) / (L8 + L4 + 1e-7)

				# Build a clear mask from LCLD1: clear pixels will be 1 (1 - 0), clouds become 0 (1 - 1)
				clear_mask = 1 - np.float32(LCLD1)

				# Combine the valid mask and clear mask:
				# Only keep NDVI values where the red band is valid and the pixel is clear
				ndvi_masked = ndvi * valid_mask * clear_mask

				# Write the resulting NDVI slice to the output TIFF
				bandOut.WriteArray(ndvi_masked.astype(np.float32), 0, int(j * jr))


							
			del driverOut
			
			print ('OK')

			# bandOut.WriteArray(ndvi)
			flocal.write(nameNdvi+'\n')

			fileBand4=None
			fileBand8=None
			shutil.rmtree(fname_L2A)
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