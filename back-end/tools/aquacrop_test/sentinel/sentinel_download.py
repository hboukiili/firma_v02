#! /usr/bin/env python

# -*- coding: iso-8859-1 -*-

import json
import time
import os, os.path, optparse,sys
from datetime import date
from osgeo import ogr
from shapely.geometry.base import geom_from_wkt
from shapely.wkt import loads 

# configuration SAT-IRR

import config


def sentinel_download(lat, lon, start_date, end_date):
	"""
		Download the products matching the given criterias from Theia if possible, or from PEPS.

		:param lat: 		latitude
		:param lon:		longitude
		:param start_date:	start date	(must be "YYYY-MM-DD")
		:param start_end:	end date	(must be "YYYY-MM-DD")
		:return:		none
	"""
	download_list_theia = sentinel_search_theia(lat, lon, start_date, end_date)
	if len(download_list_theia) == 0 :
		print ("No Theia product matching the criterias")
		sentinel_download_peps(sentinel_search_peps(lat, lon, start_date, end_date))
	else :
		sentinel_download_theia(download_list_theia)




def sentinel_tile(lat,lon):
	"""
		Find the name of Sentinel-2 tile for the given coordonates.

		:param lat: 	latitude
		:param lon: 	longitude
		:return: 	list of the names of the sentinel-2 tiles matching the given coordonates
	"""

	# Polygon shapefile used to make stats
	# a modifier
	shp = "auxiliar/sentinel_2_index_shapefile.shp"
	
	# arrays to tests Sentinel Paths
	n=[]
	npath=0
	
	wkt1 = "POINT("+str(lon)+" "+str(lat)+")"
	point1 = ogr.CreateGeometryFromWkt(wkt1)
	shapely_point=geom_from_wkt(wkt1)		
	# Open the shapefile
	
	try:
		driver = ogr.GetDriverByName("ESRI Shapefile")
		shapef = driver.Open(shp)
		lyr = shapef.GetLayer() #equivalent a datasource.GetLayer(0)
		elements= lyr.GetFeatureCount()
		
		# for each element of the shapefile 
		for ilyr in range(elements):
			poly = lyr.GetNextFeature()
			geom = loads(poly.geometry().ExportToWkt())	
			if geom: # if the geometry is not empty.		
				intersection = geom.intersection(shapely_point)
				if intersection.is_empty==False: # if this polygon intersect with our point	
					# Test if this name has not already been selected
					sentinel_name=poly.GetField("Name")
					trouve=False
					for i in range(0,npath):
						if n[i]==sentinel_name: trouve=True
					# If the name has not been selected, keep the name definition
					if trouve==False:
						n.append(sentinel_name)
						npath=npath+1
		return n
	except:
		return([])


def sentinel_search_peps(lat, lon, start_date, end_date):
	"""
		Search for sentinel-2 products matching the given coordonates and dates from PEPS.

		:param lat: 		latitude
		:param lon:		longitude
		:param start_date:	start date	(must be "YYYY-MM-DD")
		:param end_date:	end date	(must be "YYYY-MM-DD")
		:return:		list of ids or products matching the given parameters
	"""

	query_geom='lat=%f\&lon=%f'%(lat,lon)
	if os.path.exists('search.json'):
		os.remove('search.json')
    
	search_catalog='curl -k -o search.json https://peps.cnes.fr/resto/api/collections/S2/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500'%(query_geom,start_date,end_date)
	print (search_catalog)
	os.system(search_catalog)
	time.sleep(10)
	
	# Filter catalog result
	with open('search.json') as data_file:    
		data = json.load(data_file)

	#Sort data
	download_list={}
	for i in range(len(data["features"])):    
		print (data["features"][i]["properties"]["productIdentifier"],data["features"][i]["id"],data["features"][i]["properties"]["startDate"])
		prod=data["features"][i]["properties"]["productIdentifier"]
		feature_id=data["features"][i]["id"]
		
		download_list[prod]=feature_id
	
	return download_list


def sentinel_search(start_date, end_date):
	"""
		Search for sentinel-2 products matching the authorized_landsat list from config.py.

		:param start_date:	start date	(must be "YYYY-MM-DD")
		:param end_date:	end date	(must be "YYYY-MM-DD")
		:return:		list of ids or products matching the given parameters
	"""
	# les bbox des imgs à télécharger sont tirées de la liste Landsat autorisée​

	driver = ogr.GetDriverByName("ESRI Shapefile")
	shapef = driver.Open('/var/www/Satirr/SAMIR_python/auxiliar/wrs2_descending.shp')
	lyr = shapef.GetLayer() #equivalent a datasource.GetLayer(0)
	elements= lyr.GetFeatureCount()	
	# for each element of the shapefile
	download_list={}
	for ilyr in range(elements):
		poly = lyr.GetNextFeature()
		PR=poly.GetField("PR")
		if str(PR) in config.L8_authorized:
			geom = poly.GetGeometryRef()
			if geom: # if the geometry is not empty.
				env = geom.GetEnvelope()

			# s2=requete peps_search
			query_geom = 'box=' + str(env[0]) + ',' + str(env[2]) + ',' + str(env[1]) + ',' + str(env[3])
			#print (query_geom)

			search_catalog='curl -k -o search.json https://peps.cnes.fr/resto/api/collections/S2/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500'%(query_geom,start_date,end_date)
			#print (search_catalog)
			os.system(search_catalog)
			time.sleep(10)

			# Filter catalog result
			with open('search.json') as data_file:
				data = json.load(data_file)

			#Sort data
			for i in range(len(data["features"])):    
				#print (data["features"][i]["properties"]["productIdentifier"],data["features"][i]["id"],data["features"][i]["properties"]["startDate"])
				prod=data["features"][i]["properties"]["productIdentifier"]
				feature_id=data["features"][i]["id"]

				download_list[prod]=feature_id
	
	return download_list

def sentinel_search_box(Xmin, Xmax, Ymin, Ymax, start_date, end_date):
	"""
		Search for sentinel-2 products matching the authorized_landsat list from config.py.

		:Xmin, Xmax, Ymin, Ymax:	coordonates of the bbox
		:param start_date:		start date	(must be "YYYY-MM-DD")
		:param end_date:		end date	(must be "YYYY-MM-DD")
		:return:			list of ids or products matching the given parameters
	"""

	# s2=requete peps_search
	query_geom = 'box=' + str(Xmin) + ',' + str(Ymin) + ',' + str(Xmax) + ',' + str(Ymax)
	#print (query_geom)

	search_catalog='curl -k -o search.json https://peps.cnes.fr/resto/api/collections/S2/search.json?%s\&startDate=%s\&completionDate=%s\&maxRecords=500'%(query_geom,start_date,end_date)
	#print (search_catalog)
	os.system(search_catalog)
	time.sleep(10)
	

	# Filter catalog result
	with open('search.json') as data_file:
		data = json.load(data_file)
	
	download_list={}

	#Sort data
	for i in range(len(data["features"])):   
		prod=data["features"][i]["properties"]["productIdentifier"]
		feature_id=data["features"][i]["id"]
		download_list[prod]=feature_id

	return download_list

def sentinel_download_peps(download_list) :
	"""
		Download Sentinel-2 products from a list of ids.
	
		:param download_list:	a list of the ids of the products to download
		:return: 		none
	"""

	rep = "/media/SATIRR/data/inputs"


	# read authentification file
	try:
		f=open("peps.txt")
		(email,passwd)=f.readline().split(' ')
		if passwd.endswith('\n'):
			passwd=passwd[:-1]
		f.close()
	except :
		print ("error with password file")
		sys.exit(-2)

	

	if len(download_list)==0:
		print ("No Peps product matches the criteria")
	else:
		for prod in download_list.keys():
			file_exists= os.path.exists(("%s/%s.SAFE")%(rep,prod)) or  os.path.exists(("%s/%s.zip")%(rep,prod))
			tmpfile="%s/tmp.tmp"%rep
			print (tmpfile)
			get_product='curl -o %s -k -u %s:%s https://peps.cnes.fr/resto/collections/S2/%s/download/?issuerId=peps'%(tmpfile,email,passwd,download_list[prod])
			print (get_product)
			if not(file_exists):
				os.system(get_product)
				#check if binary product

				with open(tmpfile) as f_tmp:
					try:
						tmp_data=json.load(f_tmp)
						print ("Result is a text file")
						print (tmp_data)
						sys.exit(-1)
					except :
						pass
				
				os.rename("%s"%tmpfile,"%s/%s.zip"%(rep,prod))
				print ("product saved as : %s/%s.zip"%(rep,prod))
			elif file_exists:
				print ("%s already exists"%prod)


def sentinel_search_theia(lat, lon, start_date, end_date):
	"""
		Search for sentinel-2 products matching the given coordonates and dates from Theia.

		:param lat: 		latitude
		:param lon:		longitude
		:param start_date:	start date	(must be "YYYY-MM-DD")
		:param start_end:	end date	(must be "YYYY-MM-DD")
		:return:		list of ids or products matching the given parameters
	"""
	#TODO
	return ([])


def sentinel_download_theia(download_list) :
	"""
		Download Sentinel-2 products from a list of ids.
	
		:param download_list:	list of ids of products to download
		:return: 		none
	"""
	#TODO

			
