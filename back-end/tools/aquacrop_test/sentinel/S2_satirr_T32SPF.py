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
from datetime import datetime
from datetime import timedelta
import simplejson as json
import urllib
import time

from S2_ndvi import *
from S2_config import *

S2_authorized=["32SPF"]

#import shapely
#from shapely.wkt import loads 
#from shapely.geometry.base import geom_from_wkt

"""
S2_authorized=["31TCJ","31TDJ","31TCH","31TDH","31TCG","30TYM","31TBG","29SPR","29SNR","29RNQ","29RPQ","32SNE","32SPE","32SNF","32SPF","30TYP","30TXP"]

downloader="aria2"
url_search="https://scihub.copernicus.eu/apihub/search?rows=100&q="
account="michel"
passwd="michel123"
write_dir='.'
sentinel="S2"
no_download=False

path_to_sen2cor='/home/michel/sen2cor'
path_to_anaconda2 = '/home/michel/anaconda2'
sen2cor_init="export SEN2COR_HOME=%s;export SEN2COR_BIN=%s/lib/python2.7/site-packages/sen2cor-2.3.0-py2.7.egg/sen2cor;export GDAL_DATA=%s/lib/python2.7/site-packages/sen2cor-2.3.0-py2.7.egg/sen2cor/cfg/gdal_data" % (path_to_sen2cor,path_to_anaconda2,path_to_anaconda2)
"""

def S2_tile_centroid(list_tile):

	# Polygon shapefile used to make stats
	shp = os.path.join("auxiliar","sentinel_2_index_shapefile.shp")
	#shp ="sentinel_2_index_shapefile.shp"
	S2_lat = [""] * len(list_tile)
	S2_lon = [""] * len(list_tile)
	
	#wkt1 = "POINT("+str(lon)+" "+str(lat)+")"
	#point1 = ogr.CreateGeometryFromWkt(wkt1)
	#shapely_point=geom_from_wkt(wkt1)		

	# Open the shapefile
	try:
		driver = ogr.GetDriverByName("ESRI Shapefile")
		shapef = driver.Open(shp)
		lyr = shapef.GetLayer() #equivalent a datasource.GetLayer(0)

		for feat in lyr:
			attribute = feat.GetField("Name")
			if attribute in list_tile:
				ind=list_tile.index(attribute)
				geom = feat.GetGeometryRef()
				centroid=geom.Centroid()
				print(attribute,centroid.GetPoint())
				S2_lon[ind] = centroid.GetPoint()[0]
				S2_lat[ind] = centroid.GetPoint()[1]
		return(S2_lat,S2_lon)
	except:
		return([],[])

#get URL, name and type within xml file from Scihub
def get_elements(xml_file):
	urls=[]
	contentType=[]
	name=[]
	with open(xml_file) as fic:
		line=fic.readlines()[0].split('<entry>')
		for fragment in line[1:]:
			urls.append(fragment.split('<id>')[1].split('</id>')[0])
			contentType.append(fragment.split('<d:ContentType>')[1].split('</d:ContentType>')[0])
			name.append(fragment.split('<title type="text">')[1].split('</title>')[0])
			#print name
	os.remove(xml_file)
	return urls,contentType,name

# recursively download file tree of a Granule
def download_tree(rep,xml_file,wg,auth,wg_opt,value):
	urls,types,names=get_elements(xml_file)
	for i in range(len(urls)):
		urls[i]=urls[i].replace("eu/odata","eu/apihub/odata") #patch the url
		if types[i]=='Item' and not 'ECMWFT' in names[i]:
			nom_rep="%s/%s"%(rep,names[i])
			if not(os.path.exists(nom_rep)):
				os.mkdir(nom_rep)
			commande_wget='%s %s %s%s "%s"'%(wg,auth,wg_opt,'files.xml',urls[i]+"/Nodes")
			print(commande_wget)
			os.system(commande_wget)
			while os.path.getsize("files.xml")==0 : #in case of "bad gateway error"
				os.system(commande_wget)
			download_tree(nom_rep,'files.xml',wg,auth,wg_opt,value)
		else:
			commande_wget='%s %s %s%s "%s"'%(wg,auth,wg_opt,rep+'/'+names[i],urls[i]+'/'+value)
			os.system(commande_wget)
			while os.path.getsize(rep+'/'+names[i])==0 : #retry download in case of a Bad Gateway error"
				os.system(commande_wget)

def get_dir(dir_name,dir_url,product_dir_name,wg,auth,wg_opt,value):
	dir=("%s/%s"%(product_dir_name,dir_name))
	dir_url=dir_url.replace("eu/odata","eu/apihub/odata")  #patch the url
	if not(os.path.exists(dir)) :
		os.mkdir(dir)
	commande_wget='%s %s %s%s "%s"'%(wg,auth,wg_opt,'temp.xml',dir_url)
	print(commande_wget)
	os.system(commande_wget)
	while os.path.getsize("temp.xml")==0 : #in case of "bad gateway error"
		os.system(commande_wget)
	download_tree(product_dir_name+'/'+dir_name,"temp.xml",wg,auth,wg_opt,value)
  
def Theia_S2_download(lat,lon,level):
	"""
	https://raw.githubusercontent.com/olivierhagolle/theia_download
	"""

	#=====================
	# proxy
	#=====================
	curl_proxy = ""
	if "proxy" in config_theia.keys():
		curl_proxy = str("-x %s --proxy-user %s:%s" % (config_theia["proxy"],config_theia["login_proxy"],config_theia["password_proxy"]))

	#============================================================
	# get a token to be allowed to bypass the authentification.
	# The token is only valid for two hours. If your connection is slow
	# or if you are downloading lots of products, it might be an issue
	#=============================================================
	get_token='curl -k -s -X POST %s --data-urlencode "ident=%s" --data-urlencode "pass=%s" %s/services/authenticate/>token.json'%(curl_proxy, config_theia["login_theia"], config_theia["password_theia"], config_theia["serveur"])

	#print get_token

	os.system(get_token)

	token=""
	token_type=config_theia["token_type"]
	with open('token.json') as data_file:
		try :
			if token_type=="json":
				token_json = json.load(data_file)
				token=token_json["access_token"]

			elif token_type=="text":
				token=data_file.readline()

			else:
				print(str("error with config file, unknown token_type : %s" % token_type))
				return(0)
		except :
			print("Authentification is probably wrong")
			return(0)
	os.remove('token.json')

	#====================
	# search catalogue
	#====================

	if os.path.exists('search.json'):
		os.remove('search.json')

	#query=  "%s\&platform=%s\&startDate=%s\&completionDate=%s\&maxRecords=500"\%(query_geom,options.platform,start_date,end_date)
	dict_query={'lat':lat,'lon':lon}
	#dict_query['platform']=config_theia["platform"]
	dict_query['collection']=config_theia["collection"]
	dict_query['startDate']="2016-12-06"
	#dict_query['completionDate']="2017-12-31"
	dict_query['processingLevel']="LEVEL2A"
	dict_query['maxRecords']=500

	query="%s/%s/api/collections/%s/search.json?"%(config_theia["serveur"], config_theia["resto"],config_theia["collection"])+urllib.parse.urlencode(dict_query)
	print(query)
	search_catalog='curl -k %s -o search.json "%s"'%(curl_proxy,query)
	print(search_catalog)
	os.system(search_catalog)
	time.sleep(5)

	#====================
	# Download
	#====================

	n_download=0
	with open('search.json') as data_file:    
		data = json.load(data_file)

	for i in range(len(data["features"])):	
		prod=data["features"][i]["properties"]["productIdentifier"]
		feature_id=data["features"][i]["id"]

		cloudCover=int(data["features"][i]["properties"]["cloudCover"])
		
		tileid=data["features"][i]["properties"]["location"]
		date_prod=data["features"][i]["properties"]["completionDate"][0:10]
		date_prod_esa=date_prod[0:4]+date_prod[5:7]+date_prod[8:10]
		print(prod,feature_id)
		print("cloudCover:",cloudCover)

		#do not download the product if it was already downloaded and unzipped, or if no_download option was selected.
		zipped_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',prod+".zip")))
		zipped_file_esa_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',"S2?_MSIL2A_"+date_prod_esa+"*_"+tileid+"_*.zip")))

		part_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',prod+".zip.1"))) or os.path.exists(("%s")%(os.path.join(write_dir,'inputs',prod+".zip.aria2")))
		
		test_zip=zipped_file_exists is False and zipped_file_esa_exists is False and part_file_exists is False		

		unzipped_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',prod)))
		unzipped_file_esa_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',"S2?_MSIL2A_"+date_prod_esa+"*_"+tileid+"_*")))
			
		ndvi_fname = tileid+'_'+date_prod[0:4]+'.'+date_prod[5:7]+'.'+date_prod[8:10]+'_ndvi.tif'
		ndvi_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'outputs',ndvi_fname)))
		
		print(unzipped_file_exists==False,ndvi_file_exists==False,no_download==False)
					
#		file_exists=os.path.exists("%s/%s.zip"%(write_dir,prod))
		tmpfile=os.path.join(write_dir,"inputs","tmp.tmp")
		get_product='curl %s -o %s -k -H "Authorization: Bearer %s" %s/%s/collections/%s/%s/download/?issuerId=theia'%(curl_proxy,tmpfile,token,config_theia["serveur"], config_theia["resto"],config_theia["collection"],feature_id)
		print(get_product)

#		if not(file_exists):
		if test_zip  and unzipped_file_exists==False and unzipped_file_esa_exists==False and ndvi_file_exists==False and no_download==False:			
			#download only if cloudCover below maxcloud
			if cloudCover <=config_theia["maxcloud"]:
				os.system(get_product)

				#check if binary product
				fsize = os.stat(tmpfile).st_size > 500*1024*1024
				if fsize:
					n_download = n_download + 1
					os.rename(tmpfile,os.path.join(write_dir,'inputs',prod)+".zip")
					print("product saved as : %s.zip"%os.path.join(write_dir,prod))
				else:
					# small file (incomplete orbit is less than 500Mb)
					os.remove(tmpfile)
					# we create an empty file
					open(os.path.join(write_dir,'inputs',prod)+".zip", 'a').close()
#				with open(tmpfile) as f_tmp:
#					try:
#						tmp_data=json.load(f_tmp)
#						print("Result is a text file")
#						print(tmp_data)
#						pass
#					except ValueError:
#						f_tmp.close()
#						n_download = n_download + 1
#						os.rename(os.path.join(write_dir,tmpfile),os.path.join(write_dir,'inputs',prod)+".zip")
#						print("product saved as : %s.zip"%os.path.join(write_dir,prod))
#						pass
			else :
				print("cloud cover too high : %s"%(cloudCover) )
		else:
			print("%s already exists"%prod)

	os.remove('search.json')
	return(n_download)
	
	
def S2_download(lat,lon,level):

	query_results=os.path.join(write_dir,"query_results.xml")
	if os.path.exists(query_results):
		os.remove(query_results)
		
	if downloader=="aria2":
		wg='aria2c --dir / --check-certificate=false'
		auth='--http-user="%s" --http-passwd="%s"'%(account,passwd)
		search_output=" --continue -o "+query_results
		wg_opt=" -o "
		if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
			value="\$value"
		else:
			value="$value"
	else :
		wg="wget --no-check-certificate"
		auth='--user="%s" --password="%s"'%(account,passwd)
		search_output="--output-document=query_results.xml"
		wg_opt=" --continue --output-document="
		if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
			value="\\$value"
		else:
			value="$value"
			
	query='footprint:\\"Intersects(%f,%f)\\"'%(lat,lon)
	query=query + ' filename:%s*'%(sentinel)
	query= query + " producttype:%s "%level

	start_date="2017-06-01"+"T00:00:00.000Z"	# date du changement de format de distribution
	end_date="2018-01-01"+"T00:00:00.000Z"	# date du changement de format de distribution
	#end_date="NOW"	
	query_date=" ingestiondate:[%s TO %s]"%(start_date,end_date)
	#query_date=" ContentDate/Start:%s"%(start_date)
	
	query=query+query_date

	#start_date = (datetime.now()-timedelta(365)).strftime("%Y%m%d")
	
	commande_wget='%s %s %s "%s%s"'%(wg,auth,search_output,url_search,query)	
	print(commande_wget)
	
	retry=0
	ok=False
	while ok is False and retry<3:
		print(commande_wget)
		os.system(commande_wget)
		if os.path.exists(query_results):
			ok=True
		else:
			retry=retry+1
			
	if os.path.exists(query_results):
		#=======================
		# parse catalog output
		#=======================
		xml=minidom.parse(query_results)
		products=xml.getElementsByTagName("entry")
		
		for prod in products:
			ident=prod.getElementsByTagName("id")[0].firstChild.data
			print(ident)
			link=prod.getElementsByTagName("link")[0].attributes.items()[0][1] 
			#to avoid wget to remove $ special character
			link=link.replace('$value',value)
		
			for node in prod.getElementsByTagName("str"):
				(name,field)=node.attributes.items()[0]
				if field=="filename":
					filename= str(node.toxml()).split('>')[1].split('<')[0]   #ugly, but minidom is not straightforward
	
					if len(filename.split("_")) == 7:
						date_prod=filename.split('_')[-1][:8]
					else:
						date_prod = filename.split('_')[7][1:9]		
				#print("******>%s %s"%(start_date,date_prod))
	
			if date_prod>=start_date:	
	
				#print what has been found
				print("\n===============================================")
				print(filename)
				print(link)
				cloud = 0
				for node in prod.getElementsByTagName("double"):
					(name, field) = list(node.attributes.items())[0]
					if field == "cloudcoverpercentage":
						cloud = float((node.toxml()).split('>')[1].split('<')[0])
						print("cloud percentage = %5.2f %%" % cloud)				
				print("===============================================\n")
		    	
				#==================================download product
				if cloud < 75:
					commande_wget='%s %s %s%s/%s "%s"'%(wg,auth,wg_opt,os.path.join(write_dir,'inputs'),filename+".zip",link)
					#do not download the product if it was already downloaded and unzipped, or if no_download option was selected.
					zipped_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',filename+".zip")))
					part_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',filename+".zip.1"))) or os.path.exists(("%s")%(os.path.join(write_dir,'inputs',filename+".zip.aria2")))
					test_zip=zipped_file_exists is False and part_file_exists is False
					
					unzipped_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'inputs',filename)))
					ndvi_fname = filename[38:44]+'_'+date_prod[0:4]+'.'+date_prod[4:6]+'.'+date_prod[6:8]+'_ndvi.tif'
		
					ndvi_file_exists = os.path.exists(("%s")%(os.path.join(write_dir,'outputs',ndvi_fname)))
					print(unzipped_file_exists==False,ndvi_file_exists==False,no_download==False)
					print(os.path.exists(("%s")%(os.path.join(write_dir,'inputs',filename))),filename[38:44]+'_'+date_prod[0:4]+'.'+date_prod[4:6]+'.'+date_prod[6:8]+'_ndvi.tif')
					
					if test_zip  and unzipped_file_exists==False and ndvi_file_exists==False and no_download==False:
						print(commande_wget)
						os.system(commande_wget)
	    		
			
	#os.system("python Sentinel_download2.py -a apihub.txt  --lat 43.6 --lon 1.44 -d 2016")
	
def S2_Process_L1C(fname):
	"""
		Uncompress the file and apply Sen2cor and call ndvi computation
		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""	
	fname2=fname.split(os.sep)[-1]
	fname_dir_L1C=os.path.join(write_dir,'inputs',fname2[:-4])
	fname_dir_L2A=os.path.join(write_dir,'inputs',fname2[:-4].replace("L1C","L2A"))
	print(fname_dir_L1C,fname_dir_L2A)

	ladate = fname2[45:53]
	ndvi_fname = fname2[38:44]+'_'+ladate[0:4]+'.'+ladate[4:6]+'.'+ladate[6:8]+'_ndvi.tif'
	
	if os.path.exists(os.path.join(write_dir,'outputs',ndvi_fname)) is False:
		print("Le fichier %s n'existe pas. Il faut le creer à partir du niveau L1C"%os.path.join(write_dir,'outputs',ndvi_fname))
		
		if os.path.exists(fname) is False or os.path.isdir(fname_dir_L1C) is True:
			print("**** %s or %s already exists, I don't unzip"%(fname, fname_dir_L1C))
		else:
			print("unzip %s -d %s"%(fname,os.path.join(write_dir,'inputs')))
			os.system("unzip %s -d %s"%(fname,os.path.join(write_dir,'inputs')))
		
		if os.path.isdir(fname_dir_L2A) is False and os.path.isdir(fname_dir_L1C) is True:
			commande='export PATH="%s/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"; %s; L2A_Process %s --resolution=10' % (path_to_anaconda2, sen2cor_init, fname_dir_L1C)
			os.system(commande)
			
			shutil.rmtree(fname_dir_L1C)
			
			#print('export PATH="%s:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin";source /home/michel/sen2cor/L2A_Bashrc; L2A_Process %s --resolution=10' % (path_to_anaconda2, fname_dir_L1C))
			#os.system("source %s/L2A_Bashrc; L2A_Process %s --resolution=10" % (path_to_sen2cor,fname_dir_L1C))
			# *=*=*=*=*=*=*=*=*=*=*=*==*
			# os.system('rmdir -r %s'%fname_dir_L1C)
		else:
			print('the L2A directory already exists')

def S2_Process_L2A(fname):
	"""
		Uncompress the file and apply Sen2cor and call ndvi computation
		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""	
	fname2=fname.split(os.sep)[-1]
	fname_dir_L2A=os.path.join(write_dir,'inputs',fname2[:-4])
	print(fname_dir_L2A)

	ladate = fname2[45:53]
	ndvi_fname = fname2[38:44]+'_'+ladate[0:4]+'.'+ladate[4:6]+'.'+ladate[6:8]+'_ndvi.tif'
	
	if os.path.exists(os.path.join(write_dir,'outputs',ndvi_fname)) is False:
		print("Le fichier %s n'existe pas. Il faut le creer à partir du niveau L2A"%os.path.join(write_dir,'outputs',ndvi_fname))
		
		if os.path.exists(fname) is False or os.path.isdir(fname_dir_L2A) is True:
			print("**** %s or %s already exists, I don't unzip"%(fname, fname_dir_L2A))
		else:
			print("unzip %s -d %s"%(fname,os.path.join(write_dir,'inputs')))
			os.system("unzip %s -d %s"%(fname,os.path.join(write_dir,'inputs')))

def Theia_S2_Process_L2A(fname):
	"""
		Uncompress the file and apply Sen2cor and call ndvi computation
		:param sen2corDir: 	Directory of the processed granule

		..warnings:: Gdal must be configure to open JP2 files.
	"""	
	if os.stat(fname).st_size > 0 : 
		fname2=fname.split(os.sep)[-1]
		fname_dir_L2A=os.path.join(write_dir,'inputs',fname2[:-4])
		print(fname_dir_L2A)
	
		ladate = fname2.split('_')[1].split('-')[0]
		tile=fname2.split('_')[3]
		ndvi_fname = tile+'_'+ladate[0:4]+'.'+ladate[4:6]+'.'+ladate[6:8]+'_ndvi.tif'
		
		if os.path.exists(os.path.join(write_dir,'outputs',ndvi_fname)) is False:
			print("Le fichier %s n'existe pas. Il faut le creer à partir du niveau L2A"%os.path.join(write_dir,'outputs',ndvi_fname))
			
			if os.path.exists(fname) is False or os.path.isdir(fname_dir_L2A) is True:
				print("**** %s or %s already exists, I don't unzip"%(fname, fname_dir_L2A))
			else:
				print("unzip %s -d %s"%(fname,os.path.join(write_dir,'inputs')))
				os.system("unzip %s -d %s"%(fname,os.path.join(write_dir,'inputs')))
			
if __name__ == "__main__":
	print("****************************************************************************")
	print(datetime.now())
	print("****************************************************************************")
	
	
	# ----- S2 ESA ----
	S2_lat, S2_lon=S2_tile_centroid(S2_authorized)
	print(S2_lat)
	print(S2_lon)

	for i in range(len(S2_authorized)):
		tile=S2_authorized[i]
		lat=S2_lat[i]
		lon=S2_lon[i]
		level="S2MSI2A"
		print("-----> DOWNLOAD ESA Level %s Tile %s <-----"%(level,tile))

	#	S2_download(lat,lon,level)
		
		list_zip=glob.glob(os.path.join(write_dir,'inputs',"*%s*.zip"%tile))
		for fname in list_zip:
			S2_Process_L2A(fname)
	# --- L2A -> NDVI ---

	list_L2A = glob.glob(os.path.join(write_dir,'inputs',"S2?_MSIL2A*SAFE"))
	print(list_L2A)
	dir_NDVI=os.path.join(write_dir,'outputs')
	flocal=os.path.join(dir_NDVI,'flocal.txt')	
	for L2A in list_L2A:
		print(L2A)
		fname=S2_ndvi(L2A,dir_NDVI,flocal)

	# ----- S2 THEIA ----
	S2_lat, S2_lon=S2_tile_centroid(Theia_S2_authorized)

	for i in range(len(Theia_S2_authorized)):
		tile=Theia_S2_authorized[i]
		lat=S2_lat[i]
		lon=S2_lon[i]
		level="LEVEL2A"
		print("-----> DOWNLOAD THEIA Level %s Tile %s <-----"%(level,tile))

		Theia_S2_download(lat,lon,level)
		
		list_zip=glob.glob(os.path.join(write_dir,'inputs',"*%s*.zip"%tile))
		for fname in list_zip:
			Theia_S2_Process_L2A(fname)

	# --- L2A -> NDVI ---

	list_L2A = glob.glob(os.path.join(write_dir,'inputs',"SENTINEL2*_D_*"))
	print(list_L2A)
	dir_NDVI=os.path.join(write_dir,'outputs')
	flocal=os.path.join(dir_NDVI,'flocal.txt')	
	for L2A in list_L2A:
		print(L2A)
		fname=S2_ndvi_theia(L2A,dir_NDVI,flocal)			
		
	"""	
	for i in range(len(S2_authorized)):
		tile=S2_authorized[i]
		lat=S2_lat[i]
		lon=S2_lon[i]
		level="S2MSI1C"		
		print("-----> DOWNLOAD Level %s Tile %s <-----"%(level,tile))

		S2_download(lat,lon,level)
		
		list_zip=glob.glob(os.path.join(write_dir,'inputs',"*%s*.zip"%tile))
		for fname in list_zip:
			S2_Process_L1C(fname)
	"""

	"""
	for i in range(len(S2_authorized)):
		tile=S2_authorized[i]
		list_zip=glob.glob(os.path.join(write_dir,'inputs',"*%s*.zip"%tile))
		for fname in list_zip:
			S2_Process(fname)
	"""

	"""
	list_L2A = glob.glob(os.path.join(write_dir,'inputs',"*L2A*SAFE"))
	dir_NDVI=os.path.join(write_dir,'outputs')
	flocal=os.path.join(dir_NDVI,'flocal.txt')	
	for L2A in list_L2A:
		S2_ndvi(L2A,dir_NDVI,flocal)
	"""
