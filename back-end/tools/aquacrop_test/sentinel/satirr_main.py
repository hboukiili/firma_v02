# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 15:11:32 2014


This is the SAT-IRR main program.

First step is to initialize the plot description table and the data table (satirr.caracteristique) for FAO station id and profiles, WMO stations id and data, NDVI landsat ID and data
The Second step is to update the plot data
The third step is to make the calculations of kcb, fc and hydric budget

"""

import sys
import glob
import psycopg2
import logging
from osgeo import gdal, osr, ogr
import os
from datetime import datetime,timedelta
from scipy import interpolate
import numpy as np

import config
import landsat_download as L8
import sentinel_download as S2
from landsat8_process import landsat8_process
import landsat_theia_process
import sentinel_process as S2_P
import pg2shp
from ndvi_shp_stat import ndvi_shp_stat
from ndvi_push_to_pgsql import ndvi_push
from wmo_nearest_station import wmo_nearest_station,fao_nearest_station
from ndvi_kcbfc import ndvi_kcbfc
from satirr_bilanhyd import satirr_bilanhyd
import meteo_ogimet
import meteo_files
from ndvi_lastimg import ndvi_lastimg
from satirr_weather_forecast import satirr_weather_forecast
from satirr_log import satirr_log


#================================================================
# ======== UPDATE COUCHES for LANDSAT IDs =======================
#================================================================

def satirr_init_idL8(plotid=''):

	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("================ SATIRR INIT ID L8 =========================")

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()

		# ------ test if there are some polygonns that don't have their landsat tiles setted up yet! ----

		#sql = 'SELECT sum(nb) FROM ( SELECT count(idcouche) nb FROM satirr.couches UNION ALL SELECT count(idcouche) * -1 nb FROM satirr.image ) as A'
		sql = "SELECT ST_AsText(ST_centroid(geometry)), C.idcouche FROM satirr.couches C EXCEPT SELECT ST_AsText(ST_centroid(geometry)), C.idcouche FROM satirr.couches C, satirr.image I WHERE C.idcouche=I.idcouche"
		cur.execute(sql)          
		ver = cur.fetchall()
		logging.info(" %s",str(ver))
		
		#if ver[0][0]>0:
		if len(ver)>0:
			# look for the path/row of each plot based on its centroid
			connString2 = "PG: host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
			sql = "SELECT ST_AsText(ST_centroid(geometry)), C.idcouche FROM satirr.couches C EXCEPT SELECT ST_AsText(ST_centroid(geometry)), C.idcouche FROM satirr.couches C, satirr.image I WHERE C.idcouche=I.idcouche"
			# commande sql pour tester l'ensemble des parcelles
			#sql = "SELECT ST_AsText(ST_centroid(geometry)), C.idcouche FROM satirr.couches C"
	
			conn = ogr.Open(connString2)
			layer = conn.ExecuteSQL(sql)
		
			feat = layer.GetNextFeature()
			while feat is not None:
				id = feat.GetField('idcouche')
				if plotid=='' or str(plotid)==str(id) :
					print(id)
					# on a demandé le centroide à postgis
					geom = feat.GetGeometryRef()
					lon = geom.GetPoint(0)[0]
					lat = geom.GetPoint(0)[1]
					#path, row = L8.landsat_tile_wrs2(lon,lat)
					#logging.info(" ====> L8 PATHROW, id=%d -> Path=%s, Row=%s",id,str(path),str(row))
					sqlsat="select distinct path,row from satellite.landsat8 where ST_Intersects(ST_GeometryFromText('SRID=4326;POINT(" + str(lon) + ' ' + str(lat) + ")'),geom)"
					cur.execute(sqlsat)          
					ver = cur.fetchall()
					logging.info(" ====> L8 PATHROW, id=%d -> Path=%s",id,str(ver))

					#for i in range(path.__len__()):
					for i in range(ver.__len__()):
						bb = str("%03d%03d"%(ver[i][0],ver[i][1]))
						if bb in config.L8_authorized:
							logging.info(" ====> L8 Authorized:%s",bb)
							#sql = "SELECT idimage FROM satirr.image WHERE idimage = CAST( " + str("%03d%03d"%(path[0],row[0])) + " as character varying) "
							#cur.execute(sql)
							#ver = cur.fetchall()
							#if len(ver) == 0 :
							sql = "INSERT INTO satirr.image(idcouche,idimage,idsat) VALUES("+str(id)+","+bb+", 'L8')"
							#deshabilité pour activer S2 uniquement
							cur.execute(sql)
							con.commit()
						else :
							logging.info(" ====>Unauthorized Path Row : " + bb)

			
					'''#TODO : tiles = L8.landsat_theia_tile(lat,lon)
					logging.info(" ====> TILE, id=%d -> Tile=%s",id,str(tiles))
					for tile in tiles :
						if tile in config.L8_theia_authorized:
							logging.info(" ====>Authorized:%s",tile)
							sql="INSERT INTO satirr.image(idcouche,idimage,idsat) VALUES("+str(id)+", \'"+str(tile)+"\', 'L8_Theia')"
							cur.execute(sql)
							con.commit()
						else :
							logging.info(" ====>Unauthorized Tile : "+tile)'''
	
			
					#tiles = S2.sentinel_tile(lat,lon)
					#logging.info(" ====> S2 TILE, id=%d -> Tile=%s",id,str(tiles))
					sqlsat="select name from satellite.sentinel_2a where ST_Intersects(ST_GeometryFromText('SRID=4326;POINT(" + str(lon) + ' ' + str(lat) + ")'),geom)"
					cur.execute(sqlsat)          
					tiles = cur.fetchall()
					logging.info(" ====> S2 TILE, id=%d -> Path=%s",id,str(tiles))
					for tile in tiles :
						tile=tile[0]
						if tile in config.S2A_authorized:
							logging.info(" S2 ====> Authorized:%s",tile)
							sql = "SELECT idimage FROM satirr.image WHERE idcouche="+str(id)+" and idimage = \'" + tile + "\'"
							cur.execute(sql)
							ver = cur.fetchall()
							if len(ver) == 0 :
								sql="INSERT INTO satirr.image(idcouche,idimage,idsat) VALUES("+str(id)+", \'"+str(tile)+"\', 'S2A')"
							cur.execute(sql)
							con.commit()
						else :
							logging.info(" S2 ====> Unauthorized Tile : "+tile)
				feat.Destroy()
				feat = layer.GetNextFeature()
		
			conn.Destroy()
			
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()	
		

# sql_or: concatener une liste de choses avec des OR.
# entrée tableau ver[][], string val: valeur à selectionner
# exemple de sortie: '(idcouche=77 or idcouche=87)

def sql_or(ver2,val):

	if ver2.__len__()==0: return(val+'=-999')
	if ver2.__len__()==1: return(val+'='+str(ver2[0][0]))
	
	sel='('
	
	for row2 in ver2:
		sel=sel+val+'='+str(row2[0])+' or '
	
	sel=sel[0:sel.__len__()-4]+')'
	
	return(sel)
	

#================================================================
# ================ INITIALIZE NDVIs =============================
#================================================================

def satirr_init_ndviL8(sql_select=' and C.initialiser_ndvi=0',plotid=""):
	"""
	satirr_init_ndviL8(sql_select=' and C.initialiser_ndvi=0',plotid="")
	
	Cette fonction se charge de télécharger les images satellites (L8A, L8 niveau 2 de THEIA, S2 niveau 2 de THEIA puis de les traiter
	Cette fonction ne doit JAMAIS être appellée depuis l'interface
	
	parametres: 
		sql_select est utilisé pour faire des tests
		plotid permet de faire la mise à jour en invoquant l'identifiant d'une parcelle 
	"""
	
	global datetime
	global timedelta

	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("================ SATIRR INIT NDVI L8 ========================")

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		
		if plotid!='':
			sql="UPDATE satirr.couches SET modis = 'Loading images' where idcouche=" + str(plotid)
			cur.execute(sql)
			con.commit()		

		# ------ test if there are some polygons to initialize NDVI : Plots that has been sowed/planted (date) and not initialized yet (initialiser_ndvi)----
		if plotid == '':
			sql = 'select count(*) from satirr.couches C where date is not NULL ' + sql_select
		else:
			sql = 'select count(*) from satirr.couches where date is not NULL and idcouche=' + str(plotid) 

		logging.info("%s",sql)
		cur.execute(sql)
		ver = cur.fetchall()

		#if ver[0][0]>0:
		if len(ver)>0:
			# liste des images à récupérer
			if plotid == '':
				sql='SELECT DISTINCT ON (idimage) idimage, idsat FROM satirr.couches C, satirr.image I WHERE C.date is not NULL AND I.idcouche=C.idcouche ' + sql_select
			else:
				sql='SELECT DISTINCT ON (idimage) idimage, idsat FROM satirr.couches C, satirr.image I WHERE C.date is not NULL AND I.idcouche=C.idcouche and C.idcouche = '+ str(plotid)
			logging.info("%s",sql)
			
			cur.execute(sql)
			ver = cur.fetchall()

			for row in ver:
				idsat = row[1]

				if idsat == 'L8':
					pr = row[0]
					path_L8 = [int(pr[0:3])]
					row_L8 = [int(pr[3:6])]

					if pr in config.L8_authorized:

						logging.info(" ====> INIT pathrow %s",pr)
			
						# date de début pour cette image
						if plotid == '':
							#sql="SELECT min(date) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND I.idcouche=C.idcouche "+sql_select
							sql="SELECT min(date) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND C.date is not NULL AND I.idcouche=C.idcouche " + sql_select
						else:
							sql="SELECT min(date) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND C.date is not NULL AND I.idcouche=C.idcouche and C.idcouche = " + str(plotid)

						cur2 = con.cursor()
						cur2.execute(sql)
						ver2 = cur2.fetchall()	
				
						#if ver2[0][0]!=None:
						if len(ver2)>0:
							dateini = ver2[0][0]
							logging.info(" ====> SATIRR_INIT date %s",dateini)
					
							# list images to download for a period of time. If a Local Ndvi file already exists, L8 image is not added into this list

							date_ini = datetime.strptime(dateini, "%Y-%m-%d")-timedelta(days = 16)
							if plotid!='':
								date_end = date_ini+timedelta(days = 365+16)
							else:
								date_end = datetime.now()
							
							list_ndvi_local=L8_list_and_process(path_L8,row_L8,date_ini,date_end,plotid)
							
							ndvi_moyen(list_ndvi_local, pr, sql_select, plotid, idsat)
						
					
					else:
						logging.info("%s is not an authorized Path/Row",pr)
				"""
				elif idsat == 'L8_Theia':

					tile = row[0]

					if tile in config.L8_theia_authorized:

						logging.info("L8_Theia : %s is an authorized tile",tile)

						logging.info(" ====> INIT tile %s",tile)
			
						# date de début pour cette image
						#sql="SELECT min(date), geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '1 year' AND I.idcouche=C.idcouche AND initialiser_ndvi = 0 GROUP BY C.geometry"
						#sql="SELECT min(date), geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND I.idcouche=C.idcouche "+sql_select
						if plotid == '':
							sql="SELECT min(date), geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL  AND I.idcouche=C.idcouche " + sql_select
						else:
							sql="SELECT min(date), geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL  AND I.idcouche=C.idcouche and C.idcouche=" + str(plotid)
						cur2 = con.cursor()
						cur2.execute(sql)
						ver2 = cur2.fetchall()	
				
						#if ver2[0][0]!=None:
						if len(ver2)>0:
							dateini = ver2[0][0]

							#Get the dates
							date = datetime.strptime(dateini, "%Y-%m-%d") - timedelta(days=16)
							date_ini = date.strftime("%Y-%m-%d")
							date = datetime.now()
							date_end = date.strftime("%Y-%m-%d")
							
							logging.info(" ====> SATIRR_INIT date %s",dateini)
							
							list_ndvi_local=L8THEIA_list_and_process(ver2[0][1],date_ini,date_end,plotid)

							ndvi_moyen(list_ndvi_local, tile, sql_select, plotid, idsat)

					else:
						logging.info("%s is not an authorized tile",tile)
				"""

				if idsat == 'S2A': #### hnaaaaa

					tile = row[0]

					if tile in config.S2A_authorized:

						logging.info("%s is an authorized tile",tile)
						logging.info(" ====> INIT S2 tile %s",tile)
			
						# date de début pour cette image
						if plotid == '':
							#sql="SELECT min(date) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND I.idcouche=C.idcouche "+sql_select
							sql="SELECT min(date) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND I.idcouche=C.idcouche " + sql_select
						else:
							sql="SELECT min(date) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND I.idcouche=C.idcouche and C.idcouche = " + str(plotid)

						#if plotid == '':
						#	#sql="SELECT min(date), ST_AsEWKT(geometry) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '1 year' AND I.idcouche=C.idcouche AND initialiser_ndvi = 0 GROUP BY C.geometry"
						#	#sql="SELECT min(date), ST_AsEWKT(geometry) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND I.idcouche=C.idcouche "+sql_select
						#	sql="SELECT min(date), ST_AsEWKT(geometry) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' - interval '4 year' AND I.idcouche=C.idcouche " + sql_select
						#else:
						#	sql="SELECT min(date), ST_AsEWKT(geometry) FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' - interval '4 year' AND I.idcouche=C.idcouche and C.idcouche=" + str(plotid)
							
						cur2 = con.cursor()
						cur2.execute(sql)
						ver2 = cur2.fetchall()	
				
						#if ver2[0][0]!=None:
						if len(ver2)>0:
							dateini=ver2[0][0]

							#Get the dates
							date=datetime.strptime(dateini, "%Y-%m-%d")-timedelta(days=16)
							date_ini = date.strftime("%Y-%m-%d")
							date=datetime.now()
							date_end = date.strftime("%Y-%m-%d")
							
							logging.info(" ====> SATIRR_INIT S2 date %s",dateini)
							
							list_ndvi_local = S2A_list(tile,date_ini,date_end,plotid)

							ndvi_moyen(list_ndvi_local, tile, sql_select, plotid, idsat)

					else:
						logging.info("%s is not an authorized tile",tile)		

	except :
	    logging.error("ERROR in init_ndviL8")
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()	

def S2A_list(tile, date_ini, date_end, plotid=""):
	
	landsat_local = os.path.join(config.SATIRR,"S2","S2_local.txt")

	liste = glob.glob(os.path.join(config.SATIRR,"S2/outputs")+os.sep+'T'+tile+"*_ndvi.tif")
	
	with open(landsat_local, 'w') as flocal:
		for local_filename in liste:
			flocal.write(local_filename)
			flocal.write('\n')
		flocal.close()
		
	return(landsat_local)



def S2A_list_and_process(geom, date_ini, date_end, plotid=""):
	
	"""
	geom: the geometry in WKT
	"""

	landsat_local = os.path.join(config.SATIRR,"output","landsat_local.txt")

	#Get the bbox
	parcelle = geom.split("(")[2]#Get rid of "POLYGON(("
	parcelle = parcelle.split(")")[0]#Get rid of "))"
	listePoints = parcelle.split(",")#Split in points
	#initialize the 4 bbox points
	Xmin = listePoints[0].split()[0]
	Xmax = listePoints[0].split()[0]
	Ymin = listePoints[0].split()[1]
	Ymax = listePoints[0].split()[1]
	for point in listePoints:
		X = point.split()[0]
		Y = point.split()[1]
		if X < Xmin :
			Xmin = X
		elif X > Xmax :
			Xmax = X
		if Y < Ymin :
			Ymin = Y
		elif Y > Ymax :
			Ymax = Y

	if plotid=="":
		test_Distant=True
	else:
		test_Distant=False
		
	test_Local=True

	#################################
	# DANS sentinel_search_box IL FAUT RAJOUTER LA VERIFICATION SI L4IMAGE NDVI N'EXISTE PAS EN LOCAL, et rajouter le nom de fichier dans landsat_local.txt
	##################################
	
	download_list = S2.sentinel_search_box(Xmin, Xmax, Ymin, Ymax, date_ini, date_end)

	if test_Distant:

		S2.sentinel_download_peps(download_list)

		input_dir=os.path.join(config.SATIRR,"inputs")
		output_dir=os.path.join(config.SATIRR,"output")
		landsat_local=os.path.join(config.SATIRR,"output","landsat_local.txt")

		#extract the dowloaded image
		S2_P.unzip(input_dir, input_dir)

		#get the name of the image
		for element in os.listdir(input_dir):
			if element.endswith('.SAFE') and element.startswith('S2A_OPER'):
				for element1 in os.listdir(os.path.join(input_dir,os.path.join(element,"GRANULE"))):
					if tile in element1 and not (os.path.exists(os.path.join(element1,"_satirr"))):
						nameImg = element
						nameSen2cor = element1
		
		#calculate the ndvi of the image

		S2_P.sen2corSplit(input_dir, nameImg, landsat_local)
	
	return(landsat_local)

def L8THEIA_list_and_process(geom,date_ini,date_end,plotid=""):
	"""
	geom: the geometry in WKT
	"""
	landsat_local = os.path.join(config.SATIRR,"output","landsat_local.txt")
	
	#Get the bbox
	parcelle = geom.split("(")[2]#Get rid of "POLYGON(("
	parcelle = parcelle.split(")")[0]#Get rid of "))"
	listePoints = parcelle.split(",")#Split in points
	#initialize the 4 bbox points
	Xmin = listePoints[0].split()[0]
	Xmax = listePoints[0].split()[0]
	Ymin = listePoints[0].split()[1]
	Ymax = listePoints[0].split()[1]
	
	for point in listePoints:
		X = point.split()[0]
		Y = point.split()[1]
		if X < Xmin :
			Xmin = X
		elif X > Xmax :
			Xmax = X
		if Y < Ymin :
			Ymin = Y
		elif Y > Ymax :
			Ymax = Y
	
	if plotid=="":
		test_Distant=True
	else:
		test_Distant=False
		
	test_Local=True

	#################################
	# DANS landsat_search_theia IL FAUT RAJOUTER LA VERIFICATION SI L4IMAGE NDVI N'EXISTE PAS EN LOCAL, et rajouter le nom de fichier dans landsat_local.txt
	##################################
	download_list = L8.landsat_search_theia(Xmin, Xmax, Ymin, Ymax, date_ini, date_end)
	
	if test_Distant:
		L8.landsat_download_theia(download_list)

		input_dir = os.path.join(config.SATIRR,"inputs")
		output_dir = os.path.join(config.SATIRR,"output")
		
		#extract the dowloaded image
		landsat_theia_process.unzip(input_dir, input_dir)
		#get the name of the image
		for element in os.listdir(input_dir):
			if os.path.basename(element).startswith('LANDSAT8') and tile in element and not element.endswith('.tgz'):
				nameImg = element

		#calculate the ndvi of the image
		landsat_theia_process.ndvi(nameImg, input_dir, landsat_local)
	
	return(landsat_local)

def L8_list_and_process(path_L8,row_L8,date_ini,date_end, plotid=''):
	
	logging.debug(" ====> SATIRR_LANDSAT_LIST ")
	landsat_liste = os.path.join(config.SATIRR,"output","landsat_list.txt")
	landsat_local = os.path.join(config.SATIRR,"output","landsat_local.txt")
	logging.debug(" ====> SATIRR_LANDSAT_LIST %s %s",landsat_local,landsat_liste)
	
	if plotid=="":
		test_Distant=True
	else:
		test_Distant=False
		
	test_Local=True

	L8.landsat_list_amazon(path_L8,row_L8,date_ini,date_end,landsat_liste,landsat_local,test_Local,test_Distant)
	
	if test_Distant:			
		# download new images
		outputrep = os.path.join(config.SATIRR,"inputs")
		logging.debug(" ====> SATIRR_LANDSAT_DOWNLOAD %s", outputrep)
		L8.landsat_download_amazon(landsat_liste, outputrep)
		logging.debug(" ====> SATIRR_LANDSAT_FINISH_DOWNLOAD")

		#
		# corrections atmosphériques + nuages
		# L8.landsat_process: appel de smac.py et acca.py, puis calcul ndvi et application masque nuage
		# MACCS serait introduit ici
		# --> en sortie le fichier ndvi est codé de 0 à 255 avec ndvi=(DN-100)/100 et mask=-1.
		#

		logging.debug(" ====> SATIRR_LANDSAT_PROCESS %s",landsat_liste)
		input_dir = os.path.join(config.SATIRR,"inputs")
		output_dir = os.path.join(config.SATIRR,"output")
		try:
			f = open(landsat_liste)
			lignes = f.readlines()
			if len(lignes)>0:
				for ligne in lignes:
					#image_name=ligne.split('/')[5]
					image_name=ligne[:-1]
					logging.debug("process: %s %s",image_name,ligne)
					landsat8_process(input_dir,output_dir,image_name,landsat_local)
			f.close()
		except (OSError, IOError) as e:
			print(e.args)
			pass
	
	return(landsat_local)
								
def ndvi_moyen(landsat_local, pr, sql_select, plotid, typeinput, sql_update=''):
	"""
	typeinput="L8","L8_THEIA","S2A"
	"""
		
	logging.debug(" ====> SATIRR_NDVI_MOYEN")

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		
		flocal=open( landsat_local)

		fichier=flocal.readline()
		fichier=fichier.rstrip('\n')
		logging.debug("fichier image: %s",fichier)
		if fichier.__len__()>0:
	
			try:
				ok=1
				inDs = gdal.Open(fichier) 
				proj=inDs.GetProjection()
				OutSpatialRef = osr.SpatialReference()
				OutSpatialRef.ImportFromWkt(proj)
				inDs=None
				
			except Exception as e:
				print('Error opening file %s',fichier)
				ok=0
				pass								
	
			if ok:
				if plotid == '':
					#sql="SELECT geometry,C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' and to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND I.idcouche=C.idcouche "+sql_select
					sql="SELECT C.geometry,C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND I.idcouche=C.idcouche " + sql_select + sql_update
				else:
					sql="SELECT C.geometry,C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND I.idcouche=C.idcouche and C.idcouche=" + str(plotid) + sql_update
					
				shp=pg2shp.pg2shp(sql, OutSpatialRef)

				# Polygon shapefile used to make stats. The output shapefile from pg2shp is called SHPinit.shp
				#shp = os.path.join(config.SATIRR_LOCAL,"inputs","SHPinit.shp")
				logging.debug("shapefile: %s",shp)
		
				# 
				# 2) Calculer le NDVI de ces parcelles
				# ndvi_shp_stat.py
				# -> crée un fichier texte avec les ndvi: output/Shp_init.txt

				# As we are in the INIT, we have to do this for all the images between the initial date and now.
				# the list of images may be different from the files downloaded (landsat_liste)	

				flocal.seek(0)								
				fichiers=flocal.readlines()
		
				for fichier in fichiers:
				#for infile in glob.glob(config.SATIRR+"\\output\\*"+pr+"*_ndvi.tif"):
					# récupération de la date de l'image
					fichier=fichier.rstrip('\n') # à cause du return à la fine de la ligne
					aa=fichier.split(os.sep)
					bb=aa[aa.__len__()-1]

					if typeinput == 'L8':
						year=bb[9:13]
						day=bb[13:16]
						ladate=datetime(int(year), 1, 1) + timedelta(int(day) - 1)
					elif typeinput == 'L8_THEIA':
						year=bb[20:23]
						day=bb[24:27]
						ladate=datetime(int(year), 1, 1) + timedelta(int(day) - 1)
					elif typeinput == 'S2A':
						year=bb[7:11]
						month=bb[12:14]
						day=bb[15:17]
						ladate=datetime(int(year), int(month), int(day)) 
		
					ladate=ladate.strftime('%Y-%m-%d')					
			
					NdviFilename = os.path.join(config.SATIRR,"output","Shp_Ndvi.txt")
		
					logging.debug("NdviFilename: %s %s %s",fichier,shp,NdviFilename)
					# Masque des nuages
					clouds=""
		
					ndvi_shp_stat(fichier,shp,clouds,NdviFilename,Idpol='idcouche',ladate=ladate,Ndvi=1)

					#					
					# 3) push dans la base de données
					# Requete: insert into satirr.caracteristique (idcouche, type, valeur,date,interpoler,id_source) VALUES (77,'ndvi',0.110029182879,'2014-05-24',0,18)
					#					
					print("*********** NDVI PUSH **********")
					CloudCoverMin=.3
					ndvi_push(NdviFilename,typeinput, CloudCoverMin)
					print("*********** NDVI PUSH OK!!**********")
		flocal.close()
		
		# fin de l'initialisation du ndvi 
		if sql_update == '':
		
			if plotid == '':
				#sql="SELECT C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' and to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND I.idcouche=C.idcouche "+sql_select
				sql="SELECT C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND I.idcouche=C.idcouche "+sql_select
			else:
				sql="SELECT C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND I.idcouche=C.idcouche and C.idcouche=" + str(plotid)

			cur5 = con.cursor()
			cur5.execute(sql)
			ver5 = cur5.fetchall()
			
			if len(ver5)>0:
				sel=sql_or(ver5,'idcouche')
				sql="UPDATE satirr.couches SET initialiser_ndvi = 1 where "+sel
				print("*****:",sql,ver5)
				cur6 = con.cursor()
				cur6.execute(sql)
				con.commit()
			
	except (OSError, IOError) as e:
		print(e.args)
		pass
	    
	finally:
	    
	    if con:
	        con.close()	
		
#================================================================
# ================ UPDATE NDVIs =================================
#================================================================

def satirr_update_ndviL8(sql_select=' ', plotid=''):
	
	global datetime
	global timedelta

	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("============== SATIRR UPDATE NDVI L8 ========================")

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()

		# ------ test if there are some polygons to initialize NDVI : Plots that has been sowed/planted (date) and already initialized  (initialiser_ndvi=1)----
		if plotid == '':
			sql='select count(*) from satirr.couches where date is not NULL and initialiser_ndvi=1'
		else:
			sql='select count(*) from satirr.couches where date is not NULL and initialiser_ndvi=1'
		cur.execute(sql)          
		ver = cur.fetchall()

		#if ver[0][0]>0:
		if len(ver)>0:
			# liste des images à récupérer
			sql='SELECT DISTINCT ON (idimage) idimage, idsat, C.idcouche FROM satirr.couches C, satirr.image I WHERE C.date is not NULL AND C.initialiser_ndvi = 1 AND I.idcouche=C.idcouche'
			cur.execute(sql)
			ver = cur.fetchall()
			for row in ver:
				print(ver)
				print("*****************************",row)
				idsat = row[1]
				
				if idsat == 'L8':
					pr=row[0]
					path_L8=[int(pr[0:3])]
					row_L8=[int(pr[3:6])]
					logging.info(" ====> UPDATE pathrow %s",pr)
				
					if pr in config.L8_authorized:
				
						logging.debug(" ====> UPDATE boucle1")
						# liste des couches qui correspondent à ce Path/Row
						#sql="SELECT C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND initialiser_ndvi = 1 AND I.idcouche=C.idcouche"
						sql="SELECT C.idcouche FROM satirr.couches C, satirr.image I WHERE I.idimage='"+pr+"' AND C.date is not NULL AND initialiser_ndvi = 1 AND I.idcouche=C.idcouche"
						cur2 = con.cursor()
						cur2.execute(sql)
						ver2 = cur2.fetchall()	

						# Recherche du dernier ndvi pour ce path_row
						#if ver2[0][0]!=None:
						if len(ver2)>0:
							sel=sql_or(ver2,'idcouche')
							logging.debug(" ====> UPDATE boucle2 %s",sel)
							sql="select date from satirr.caracteristique where type='ndvi' and "+sel+"  order by date desc limit 1"
							cur3 = con.cursor()
							cur3.execute(sql)
							ver3 = cur3.fetchall()	
						
							#if ver3.__len__()==1 and ver3[0][0]!=None:
							if len(ver3)>0:								
								logging.debug(" ====> UPDATE boucle3")

								dd=ver3[0][0]
								date_last_ndvi=datetime(dd.year, dd.month, dd.day)
								print(date_last_ndvi)
							
								# si il y a plus de 15 jours entre la date du dernir NDVI et aujourd'hui actualiser cette image
								#if datetime.now()-date_last_ndvi > timedelta(days=16) :
								if 1==1 :
							
									logging.info(" ====> SATIRR_UPDATE date %s",date_last_ndvi)
								
									# list images to download for a period of time. If a Local Ndvi file already exists, L8 image is not added into this list
			
									date_ini=date_last_ndvi+timedelta(days=1)
									date_end=datetime.now()
									
									list_ndvi_local=L8_list_and_process(path_L8,row_L8,date_ini,date_end)
									
									ndvi_moyen(list_ndvi_local, pr, sql_select, plotid, idsat, sql_update=' AND initialiser_ndvi = 1 ')				

					else:
						logging.info("L8 UPDATE: %s is not an authorized Path/Row",pr)
						print(config.L8_authorized)
				"""
				elif idsat == 'L8_Theia':
					tile =row[0]
				
					logging.info(" ====> UPDATE tile %s",pr)
				
					if tile in config.L8_theia_authorized:
				
						logging.debug(" ====> UPDATE boucle1")
						# liste des couches qui correspondent à ce Path/Row
						#sql="SELECT C.idcouche, C.geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND initialiser_ndvi = 1 AND I.idcouche=C.idcouche"
						sql="SELECT C.idcouche, C.geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND initialiser_ndvi = 1 AND I.idcouche=C.idcouche"
						cur2 = con.cursor()
						cur2.execute(sql)
						ver2 = cur2.fetchall()	

						# Recherche du dernier ndvi pour ce path_row
						#if ver2[0][0]!=None:
						if len(ver2)>0:
							sel=sql_or(ver2,'idcouche')
							logging.debug(" ====> UPDATE boucle2 %s",sel)
							sql="select date from satirr.caracteristique where type='ndvi' and "+sel+"  order by date desc limit 1"
							cur3 = con.cursor()
							cur3.execute(sql)
							ver3 = cur3.fetchall()	
						
							#if ver3.__len__()==1 and ver3[0][0]!=None:
							if len(ver3)>0:
								logging.debug(" ====> UPDATE boucle3")

								dd=ver3[0][0]
								date_last_ndvi=datetime(dd.year, dd.month, dd.day)
								print(date_last_ndvi)
							
								# si il y a plus de 15 jours entre la date du dernir NDVI et aujourd'hui actualiser cette image
								if datetime.now()-date_last_ndvi > timedelta(days=16) :
							
									logging.info(" ====> SATIRR_UPDATE date %s",date_last_ndvi)
								
									# list images to download for a period of time. If a Local Ndvi file already exists, L8 image is not added into this list
			
									date_ini=date_last_ndvi+timedelta(days=1)
									date_end=datetime.now()
			
									list_ndvi_local=L8_list_and_process(ver2[0][1],date_ini,date_end)
									
									ndvi_moyen(list_ndvi_local, tile, sql_select, plotid, idsat, sql_update=' AND initialiser_ndvi = 1 ')		
				"""
				if idsat == 'S2A':
					tile =row[0]
				
					logging.info(" ====> S2A UPDATE tile %s",tile)
				
					if tile in config.S2A_authorized:
				
						logging.debug(" ====> UPDATE boucle1")
						# liste des couches qui correspondent à ce Path/Row
						#sql="SELECT C.idcouche, C.geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND to_date(date,'YYYY-MM-DD') > now() - interval '4 year' AND initialiser_ndvi = 1 AND I.idcouche=C.idcouche"
						sql="SELECT C.idcouche, C.geometry FROM satirr.couches C, satirr.image I WHERE I.idimage='"+tile+"' AND C.date is not NULL AND initialiser_ndvi = 1 AND I.idcouche=C.idcouche"
						cur2 = con.cursor()
						cur2.execute(sql)
						ver2 = cur2.fetchall()	

						# Recherche du dernier ndvi pour ce path_row
						#if ver2[0][0]!=None:
						if len(ver2)>0:
							sel=sql_or(ver2,'idcouche')
							logging.debug(" ====> UPDATE boucle2 %s",sel)
							sql="select date from satirr.caracteristique where type='ndvi' and "+sel+"  order by date desc limit 1"
							cur3 = con.cursor()
							cur3.execute(sql)
							ver3 = cur3.fetchall()	
						
							#if ver3.__len__()==1 and ver3[0][0]!=None:
							if len(ver3)>0:
								logging.debug(" ====> UPDATE boucle3")

								dd=ver3[0][0]
								date_last_ndvi=datetime(dd.year, dd.month, dd.day)
								print(date_last_ndvi)
							
								# si il y a plus de 15 jours entre la date du dernir NDVI et aujourd'hui actualiser cette image
								#if datetime.now()-date_last_ndvi > timedelta(days=16) :
								if 1==1:
							
									logging.info(" ====> SATIRR_UPDATE date %s",date_last_ndvi)
								
									# list images to download for a period of time. If a Local Ndvi file already exists, L8 image is not added into this list
			
									date_ini=date_last_ndvi+timedelta(days=1)
									date_end=datetime.now()

									list_ndvi_local=S2A_list(tile,date_ini,date_end,plotid)
									
									ndvi_moyen(list_ndvi_local, tile, sql_select, plotid, idsat, sql_update=' AND initialiser_ndvi = 1 ')
						print("********* fin traitement S2A *****",tile)
						
					else:
						logging.info("S2A UPDATE: %s is not an authorized Sentinel-2 tile",tile)
						print(config.S2A_authorized)
							
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()	
#=========================================================================
# ================ INITIALIZE FAO ID AND DATA   ==========================
#=========================================================================

def satirr_init_fao(plotid=""):

	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("================ SATIRR INIT FAO ============================")

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		
		if plotid != '':
			sql="UPDATE satirr.couches SET modis = 'Init climato' where idcouche="+str(plotid)
			cur.execute(sql)
			con.commit()

		# ------ test if there are some polygonns that don't have their wmo station yet! ----
		if plotid == "":
			sql='select count(*) from satirr.couches where date is not NULL and id_fao is NULL'
		else:
			sql='select count(*) from satirr.couches where date is not NULL and idcouche='+plotid
		cur.execute(sql)          
		ver = cur.fetchall()
		
		#if ver[0][0]>0:
		if len(ver)>0:
			# si idplot non nul, on supprime les ET0 et la pluie
			if plotid!='':
				sql="delete from satirr.caracteristique where idcouche="+plotid+" and (type='ETO' or type='pluie' or type='tmin' or type='tmax' or type='tmean')"
				cur.execute(sql)
				con.commit() 
			
			# look for the path/row of each plot based on its centroid
			connString2 = "PG: host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
			if plotid == '':
				sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where date is not NULL and id_fao is NULL"
			else:
				sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where date is not NULL and idcouche="+plotid
			
			conn = ogr.Open(connString2)
			layer = conn.ExecuteSQL(sql)
		
			feat = layer.GetNextFeature()
			while feat is not None:
				id_couche=feat.GetField('idcouche')
				date_semis=feat.GetField('date')
				# on a demandé le centroide à postgis: on cherche la station WMO la plus proche et on l'introduit dans la BD
				geom=feat.GetGeometryRef()
				lon=geom.GetPoint(0)[0]
				lat=geom.GetPoint(0)[1]

				id_fao=fao_nearest_station(lat,lon)
				logging.info(" ====> FAO, id_couche=%s id_station=%s",str(id_couche),str(id_fao))

				if id_fao != "":
			
					# update the Plot Description with its FAO id
					sql="UPDATE satirr.couches SET id_fao = '"+str(id_fao)+"' where idcouche="+str(id_couche)
					#logging.debug(" ====>  %s",sql)
					cur.execute(sql)
					con.commit()  
					
					# update caracteristiques with FAO PET
					
					date_semis=datetime.strptime(date_semis, "%Y-%m-%d")
					date_fin=date_semis+timedelta(days=365)	
					PET,Tmean=satirr_PET(id_fao,date_semis,date_fin)
					
					for i in range(365):
						ladate=datetime.strftime(date_semis+timedelta(days=i), "%Y-%m-%d")
						ET0=PET[i]
						Temperature=Tmean[i]

						values = str(id_couche) + ',\'ETO\',' + str(ET0) + ',\'' + ladate + '\'' + "'CLI'"
						sql='insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
						
						values = str(id_couche) + ',\'tmean\',' + str(Temperature) + ',\'' + ladate + '\'' + "'CLI'"
						sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ')'
						
						#logging.debug(" ====>  %s",sql)
						cur.execute(sql)
						con.commit() 														

				feat.Destroy()
				feat = layer.GetNextFeature()
		
			conn.Destroy()
	
					
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()


#=========================================================================
# ================ CALCULATE THE PET for 1 year   ==========================
#=========================================================================


def satirr_PET(idstation,date_ini,date_end):
	"""									
	For a given FAO station, reads the monthly PET values from the DB and interpolate the values for one year given a starting date
	input: 
	 - idstation (str): id of the FAO station
	 - date_ini (date): starting date (sowing date)
	 - date_end (date): end date.. Not used. The calculation is made for one year

	output:
	 y[365]: (float) a time serie of interpolated PET
		
	"""
	#config.do_plots=1
	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	
	m0=(date_ini.month)-1
	day0=(date_ini.day)-1

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		sql="select distinct on (\"WMOcode\") \"January\",\"February\",\"March\",\"April\",\"May\",\"June\",\"July\",\"August\",\"September\",\"October\",\"November\",\"December\" from wmo.\"PET_total__mly\" where \"FAOcode\"='"+idstation+"'"
		
		cur.execute(sql)          
		ver = cur.fetchall()
		
		#if ver[0][0]>0:
		if len(ver)>0:
			PET=np.array(ver[0])
			PET=PET/30.
			PET=np.roll(PET,m0*-1)
			PET=PET.tolist()
			PET.insert(0,PET[11])
			PET.append(PET[0])
			PET.append(PET[1])
			print(PET)
			
			dd=range(-15,420,30)
			# effectuer l'interpolation
			s=interpolate.interp1d(dd,PET,kind='linear')
			d2=range(day0,365+day0)
			y=s(d2)

		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		sql="select distinct on (\"WMOcode\") \"January\",\"February\",\"March\",\"April\",\"May\",\"June\",\"July\",\"August\",\"September\",\"October\",\"November\",\"December\" from wmo.\"Temp_mean_mly\" where \"FAOcode\"='"+idstation+"'"

		cur2 = con.cursor()
		cur2.execute(sql)          
		ver2 = cur2.fetchall()
		
		#if ver[0][0]>0:
		if len(ver2)>0:
			Tmean=np.array(ver2[0])
			Tmean=np.roll(Tmean,m0*-1)
			Tmean=Tmean.tolist()
			Tmean.insert(0,Tmean[11])
			Tmean.append(Tmean[0])
			Tmean.append(Tmean[1])
			print(Tmean)
			
			dd=range(-15,420,30)
			# effectuer l'interpolation
			s2=interpolate.interp1d(dd,Tmean,kind='linear')
			d2=range(day0,365+day0)
			y2=s2(d2)
			
		if len(ver)>0 and len(ver2)>0:
			return(y,y2)
			
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()	
									
#=========================================================================
# ================ INITIALIZE OGIMET ID and DATA =================
#=========================================================================

def satirr_init_meteo_ogimet(plotid=""):

	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("================ SATIRR INIT OGIMET ============================")


	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()

		if plotid!='':
			sql="UPDATE satirr.couches SET modis = 'Loading weather' where idcouche="+str(plotid)
			cur.execute(sql)
			con.commit()

		# ------ test if there are some polygonns that don't have their wmo station yet! ----
		if plotid == "":
			#sql="select count(*) from satirr.couches where  date is not NULL and to_date(date,'YYYY-MM-DD') > now() - interval '1 year'  and id_station_wmo =''"
			sql="select count(*) from satirr.couches where  date is not NULL and (id_station_wmo ='' or id_station_wmo='0')"
		else:
			#sql="select count(*) from satirr.couches where date is not NULL and to_date(date,'YYYY-MM-DD') > now() - interval '1 year'  and idcouche="+plotid
			sql="select count(*) from satirr.couches where date is not NULL and idcouche="+plotid
		cur.execute(sql)          
		ver = cur.fetchall()
		
		#if ver[0][0]>0:
		if len(ver)>0:
			
			# look for the path/row of each plot based on its centroid
			connString2 = "PG: host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
			if plotid == "":
				#sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where  date is not NULL and to_date(date,'YYYY-MM-DD') > now() - interval '1 year'  and id_station_wmo =''"
				sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where  date is not NULL  and (id_station_wmo ='' or id_station_wmo='0')"
			else:
				#sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where  date is not NULL and to_date(date,'YYYY-MM-DD') > now() - interval '1 year'  and idcouche="+plotid
				sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where  date is not NULL  and idcouche="+plotid

			conn = ogr.Open(connString2)
			layer = conn.ExecuteSQL(sql)
		
			feat = layer.GetNextFeature()
			
			while feat is not None:
				id=feat.GetField('idcouche')
				# on a demandé le centroide à postgis: on cherche la station WMO la plus proche et on l'introduit dans la BD
				geom=feat.GetGeometryRef()
				lon=geom.GetPoint(0)[0]
				lat=geom.GetPoint(0)[1]

				id_station=wmo_nearest_station(lat,lon)
				logging.info(" ====> METEO, id_couche=%s id_station=%s",str(id),str(id_station))

				# si on a trouvé une station fonctionelle:
				# 1) l'indiquer dans la table couches
				# 2) charger les données meteo dans la BD, table caracteristiques

				if id_station != "":
			
					sql="UPDATE satirr.couches SET id_station_wmo = '"+str(id_station)+"' where idcouche="+str(id)
					cur.execute(sql)
					con.commit()  
					
					# si on a trouvé une station fonctionelle,charger les données Pluie et ET0 jusqu'à hier dans la BD
					nomstation='tmp'
					config.meteo_interior=1
					
					date_semis=feat.GetField('date')
					config.first=datetime.strptime(date_semis, "%Y-%m-%d")
					config.first=config.first-timedelta(days=1)
					
					config.last=config.first + timedelta(365)
					if config.last > datetime.now():
						config.last = datetime.now()

					config.meteo_file=os.path.join(config.SATIRR,"inputs",nomstation+"_et0.txt")			# name and location of the file.
					config.meteo_name=nomstation			# Station Name
					
					filename=meteo_ogimet.ogimet(id_station,plotid)
					meteo_ogimet.decode_synop(filename,id_station,plotid)
					
					# ***** only the timestep<24h is tretaed!!! *********
					if config.meteo_timestep<24: 
						print("==> Converting from raw to Daily Data..")
						meteo_files.meteo_process_raw()
						
						print("==> Calculating Reference Evapotranspiration...")
						ET0_filename=meteo_files.meteo_process_daily()


					try:
						f=open(ET0_filename)
						
						lignes=f.readlines()
						for ligne in lignes:
							l1=ligne.split(' ')
							ladate=l1[0]
							ET0=l1[2]
							pluie=l1[3]
							tmin=l1[4]
							tmax=l1[5].split('\n')[0]
							fET0=float(ET0)
							fpluie=float(pluie)
							ftmin=float(tmin)
							ftmax=float(tmax)

							if fpluie<0: pluie=0

							sql='delete from satirr.caracteristique where idcouche='+str(id)+" and date='"+ladate+"' and (type='pluie' or type='tmin' or type='tmax' or type='tmean');"

							values = str(id) + ',\'pluie\',' + str(pluie) + ',\'' + ladate + '\'' + "'WMO'"
							sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							values = str(id) + ',\'tmin\',' + str(tmin) + ',\'' + ladate + '\'' + "'WMO'"
							sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							values = str(id) + ',\'tmax\',' + str(tmax) + ',\'' + ladate + '\'' + "'WMO'"
							sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							
							if fET0>=0 and fET0<16: 
								sql=sql+'delete from satirr.caracteristique where idcouche='+str(id)+" and date='"+ladate+"' and (type='ETO');"

								values = str(id) + ',\'ETO\',' + str(ET0) + ',\'' + ladate + '\'' + "'WMO'"
								sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'		
							
							#logging.debug(" ====>  %s",sql)
							cur.execute(sql)
							con.commit() 	
							
						f.close()						

					except (OSError, IOError) as e:
						print(e.args)
						pass

				feat.Destroy()
				feat = layer.GetNextFeature()
		
			conn.Destroy()
	
					
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()

#========================================================================================================
# ================ UPDATE OGIMET (last seven days) ============================================
#========================================================================================================

def satirr_update_meteo(plotid=''):

	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("===================== SATIRR UPDATE METEO ==============================")


	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		if plotid!='':
			sql="UPDATE satirr.couches SET modis = 'Updating weather' where idcouche="+str(plotid)
			cur.execute(sql)
			con.commit()

		if plotid == '':
			#sql="select distinct on (id_station_wmo) id_station_wmo from satirr.couches where to_date(date,'YYYY-MM-DD') > now() - interval '1 year' and id_station_wmo != '' and initialiser_ndvi=1"
			sql="select distinct on (id_station_wmo) id_station_wmo from satirr.couches where id_station_wmo != '' and id_station_wmo != '0'"
		else:
			sql="select distinct on (id_station_wmo) id_station_wmo from satirr.couches where id_station_wmo != '' and id_station_wmo != '0' and idcouche=" + str(plotid)
			
		cur.execute(sql)          
		ver = cur.fetchall()

		
		for row in ver:
			print("station ogimet",str(row[0]))
			# liste des parcelles qui utilisent cette station WMO
			if plotid == '':
				sql="select idcouche,date from satirr.couches where date is not null and id_station_wmo='"+str(row[0])+"'"
			else:
				sql="select idcouche,date from satirr.couches where date is not null and id_station_wmo='"+str(row[0])+"' and idcouche=" + str(plotid)
				
			cur.execute(sql)          
			ver2 = cur.fetchall()
			
			if len(ver2)>0:
			
#			datemin=datetime.now()
#			
#			for row2 in ver2:
#				dd=datetime.strptime(row2[1], "%Y-%m-%d")
#				if dd<datemin: datemin=dd
#			
#			print(row[0],dd)

				# charger les 7 derniers jours de meteo sur ogimet dans la BD
				nomstation='tmp'
				config.meteo_interior=1
				config.last=datetime.now()
				config.first=datetime.now()-timedelta(days=7)
		
				config.meteo_file=os.path.join(config.SATIRR,"inputs",nomstation+"_et0.txt")			# name and location of the file.
				config.meteo_name=nomstation			# Station Name
				
				filename=meteo_ogimet.ogimet(str(row[0]))
				meteo_ogimet.decode_synop(filename,str(row[0]))
				
				# ***** only the timestep<24h is tretaed!!! *********
				
				if config.meteo_timestep<24: 
					meteo_files.meteo_process_raw()
					
					ET0_filename=meteo_files.meteo_process_daily()
				
				try:
					f=open(ET0_filename)
					
					lignes=f.readlines()
					for ligne in lignes:
						l1=ligne.split(' ')
						print(l1)
						ladate=l1[0]
						ET0=l1[2]
						pluie=l1[3]
						tmin=l1[4]
						tmax=l1[5].split('\n')[0]
						
						fET0=float(ET0)
						fpluie=float(pluie)
						ftmin=float(tmin)
						ftmax=float(tmax)						
				
						for row2 in ver2:
							idcouche=row2[0]

							if fpluie<0: pluie=0

							sql='delete from satirr.caracteristique where idcouche='+str(idcouche)+" and date='"+ladate+"' and (type='pluie' or type='tmin' or type='tmax' or type='tmean');"

							values = str(idcouche) + ',\'pluie\',' + str(pluie) + ',\'' + ladate + '\'' + "'WMO'"
							sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							values = str(idcouche) + ',\'tmin\',' + str(tmin) + ',\'' + ladate + '\'' + "'WMO'"
							sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							values = str(idcouche) + ',\'tmax\',' + str(tmax) + ',\'' + ladate + '\'' + "'WMO'"
							sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							
							if fET0>=0 and fET0<16: 
								sql=sql+'delete from satirr.caracteristique where idcouche='+str(idcouche)+" and date='"+ladate+"' and (type='ETO');"

								values = str(idcouche) + ',\'ETO\',' + str(ET0) + ',\'' + ladate + '\'' + "'WMO'"
								sql=sql+'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'				
							
							#logging.debug(" ====>  %s",sql)
							cur.execute(sql)
							con.commit() 	
						
					f.close()						
				except (OSError, IOError) as e:
					print(e.args)
					pass	
					
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()	

#========================================================================================================
# ================ GROWING DEGREE DAY                        ============================================
#========================================================================================================

def satirr_GDD(plotid=''):
	logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
	logging.info("===================== SATIRR GDD ==============================")


	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()

		if plotid!='':
			sql="UPDATE satirr.couches SET modis = 'Computing GDD' where idcouche="+str(plotid)
			cur.execute(sql)
			con.commit()


		# ***ZOUBAIR*** 
		# il n'est pas necessaire de faire cette première boucle 
		# supprimmer les 11 prochaines lignes et corriger les indentations pour le reste du code
		#sql="select distinct on (id_station_wmo) id_station_wmo from satirr.couches where to_date(date,'YYYY-MM-DD') > now() - interval '1 year' and id_station_wmo != '' "
		if plotid == '':
			sql="select distinct on (id_station_wmo) id_station_wmo from satirr.couches where id_station_wmo != '' "
		else:
			sql="select distinct on (id_station_wmo) id_station_wmo from satirr.couches where id_station_wmo != '' and idcouche=" + str(plotid)
			
		cur.execute(sql)
		ver = cur.fetchall()
		
		for row in ver:
			# liste des parcelles qui utilisent cette station WMO
			if plotid == '':
				sql="select idcouche,date from satirr.couches where date is not null and id_station_wmo='"+str(row[0])+"'"
			else:
				sql="select idcouche,date from satirr.couches where date is not null and id_station_wmo='"+str(row[0])+"' and idcouche=" + str(plotid)
				
			cur.execute(sql)          
			ver2 = cur.fetchall()
			
			if len(ver2)>0:
				try:
				
					for row2 in ver2:
						idcouche=row2[0]
						date_semis=row2[1]
						sql='delete from satirr.caracteristique where idcouche='+str(idcouche)+"  and (type like 'GDD%' );"
						cur.execute(sql)
						con.commit()
						
						sql = 'select gdd_tbase,gdd_tmax,gdd_phase1_min, gdd_phase1_max,gdd_phase6_min,gdd_phase6_max,gdd_phase8_min,gdd_phase8_max from satirr."descParc" where idpar='+str(idcouche)
						cur.execute(sql)          
						gdd_params = cur.fetchall()
						gdd_params=gdd_params[0]
						
						sql = "select d1 as date,tmean,tmin,tmax from (select * from"
						sql = sql + " (select distinct date as d1,valeur as tmean from satirr.caracteristique where type='tmean' and idcouche="+str(idcouche)+" and date>'"+date_semis+"' ) t1"
						sql = sql + " left join "
						sql = sql + " (select distinct date as d2,valeur as tmin from satirr.caracteristique where type='tmin' and idcouche="+str(idcouche)+" and date>'"+date_semis+"' ) t2"
						sql = sql + " on t1.d1=t2.d2 ) t3"
						sql = sql + " left join"
						sql = sql + " (select distinct date as d4,valeur as tmax from satirr.caracteristique  where type='tmax' and idcouche="+str(idcouche)+" and date>'"+date_semis+"' ) t4"
						sql = sql + " on t4.d4=t3.d1 order by date"
						logging.info("%s",sql)
  						
						cur.execute(sql)          
						ver3 = cur.fetchall()
												
						GDD = 0.
						GDD_sum = 0.
						phase1_min_date = ''
						phase1_max_date = ''
						phase6_min_date = ''
						phase6_max_date = ''
						phase8_min_date = ''
						phase8_max_date = ''
						sql=''
						for row3 in ver3:
							ladate=row3[0].strftime("%Y-%m-%d")
							tmean=row3[1]
							tmin=row3[2]
							tmax=row3[3]
							if tmin!=None and tmax!=None:
								GDD = max((min(tmax, gdd_params[1]) + tmin) / 2. - gdd_params[0], 0.)
							elif tmean!=None:
								GDD = max(min(tmean,gdd_params[1])  - gdd_params[0], 0.)
							#else:
							#	GDD is equal to previous GDD
							
							GDD_sum = GDD_sum + GDD
							
							if GDD_sum>gdd_params[2] and phase1_min_date == '':
								phase1_min_date=ladate
							if GDD_sum>gdd_params[3] and phase1_max_date == '':
								phase1_max_date=ladate
							if GDD_sum>gdd_params[4] and phase6_min_date == '':
								phase6_min_date=ladate
							if GDD_sum>gdd_params[5] and phase6_max_date == '':
								phase6_max_date=ladate
							if GDD_sum>gdd_params[6] and phase8_min_date == '':
								phase8_min_date=ladate
							if GDD_sum>gdd_params[7] and phase8_max_date == '':
								phase8_max_date=ladate
							
							values = str(idcouche) + ',\'GDD\',' + str(GDD_sum) + ',\'' + ladate + '\'' + "'SAT'"
							sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
						if sql !='':
								
							cur.execute(sql)
							con.commit()
						
							sql=''
							if phase1_min_date != '':
								values = str(idcouche) + ',\'GDD_phase1_min\',1,\'' + phase1_min_date + '\'' + "'SAT'"							
								sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							if phase1_max_date != '':
								values = str(idcouche) + ',\'GDD_phase1_max\',1,\'' + phase1_max_date + '\'' + "'SAT'"
								sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							if phase6_min_date != '':
								values = str(idcouche) + ',\'GDD_phase6_min\',1,\'' + phase6_min_date + '\'' + "'SAT'"
								sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							if phase6_max_date != '':
								values = str(idcouche) + ',\'GDD_phase6_max\',1,\'' + phase6_max_date + '\'' + "'SAT'"
								sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							if phase8_min_date != '':
								values = str(idcouche) + ',\'GDD_phase8_min\',1,\'' + phase8_min_date + '\'' + "'SAT'"
								sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
							if phase8_max_date != '':
								values = str(idcouche) + ',\'GDD_phase8_max\',1,\'' + phase8_max_date + '\'' + "'SAT'"
								sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,source) VALUES (' + values + ');'
						
							if sql!='':
								cur.execute(sql)
								con.commit()
						
				except (OSError, IOError) as e:
					logging.error("GDD1 Error %s", e)
					pass	
					
	except psycopg2.Error as e:
	    logging.error("GDD Error %s", e)
	    pass
	    
	    
	finally:
	    
	    if con:
	        con.close()	


def satirr_main():

	# reset des données de la parcelle sauf irrig et ndvi
	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()

		sql="delete  from satirr.caracteristique where type='irrigauto'" 
		cur.execute(sql)
		con.commit() 
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	    
	    
	finally:
	    if con:
	        con.close()		

	gdal.UseExceptions()
	# intialize the meteo in case of a new plot declared by the user
	try: 
		satirr_init_fao()
		# ***ZOUBAIR*** : call weather_to_plot()
		# qui effectuera forecast_to_plot(), puis wmo_to_plot(), puis insitu_to_plot()
		# supprimmer l'appel à satirr_init_meteo_ogimet()
		satirr_init_meteo_ogimet()
	except:
		pass
	
	# intialize/update L8 NDVI 
	try:
		satirr_init_idL8()
		#satirr_init_ndviL8(sql_select='')
		satirr_init_ndviL8()
	except:
		pass
	# updates ndvi up to today
	try:
		satirr_update_ndviL8()
	except:
		pass
	# updates meteo up to today
	#try:
	#	satirr_update_meteo()
	#except:
	#	pass
	# updates openlayers3 images
	try:
		ndvi_lastimg()
	except:
		pass

	# weather forecast
	#try:
	#	satirr_weather_forecast()
	#except:
	#	pass

	# Growing Degree Day
	try:
		satirr_GDD()
	except:
		pass
			
	# calculate kcb, fc and hydric budget
	try:
		ndvi_kcbfc()
	except:
		pass

	try:
		satirr_bilanhyd()
	except:
		pass

	try:
		satirr_log()
	except:
		pass
					
def satirr_actu(plotid, onlybilan):
	print(plotid,onlybilan)
	#	config.SATIRR=config.SATIRR_LOCAL
	# reset des données de la parcelle sauf irrig et ndvi
	if onlybilan == 0:
		"""
		Cette opération doit être effectuée pour un changement de date, ou une redéfinition des limites de la parcelle.
		Dans ce cas, on actualise les images ndvi, la météo et le bilan, mais on effectue pas le téléchargement ni le traitement des images
		"""
		try:
			connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
			con = psycopg2.connect(connString)
			cur = con.cursor()
			if plotid != '':
				sql="UPDATE satirr.couches SET modis = 'Updating' where idcouche="+str(plotid)
				cur.execute(sql)
				con.commit()
				sql="UPDATE satirr.couches SET initialiser_ndvi = 0 where idcouche="+str(plotid)
				cur.execute(sql)
				con.commit()
			sql="delete  from satirr.caracteristique where type!='irrigation' and idcouche="+plotid
			cur.execute(sql)
			con.commit() 
			sql="delete  from satirr.image where idcouche="+plotid
			cur.execute(sql)
			con.commit() 
		except psycopg2.Error as e:
			logging.error("Error %s", e)
			pass
		finally:
			if con:
				con.close()

		# intialize the meteo in case of a new plot declared by the user
		try:
			satirr_init_fao(plotid)
		except:
			pass

		try:
			# ***ZOUBAIR*** : call weather_to_plot(plotid)
			# qui effectuera forecast_to_plot(plotid), puis wmo_to_plot(plotid), puis insitu_to_plot(plotid)
			# supprimmer l'appel à satirr_init_meteo_ogimet(plotid)
			satirr_init_meteo_ogimet(plotid)
		except:
			pass

		# intialize/update L8 NDVI 
		try:
			satirr_init_idL8(plotid=plotid)
		except:
			pass
		try:
			satirr_init_ndviL8(plotid=plotid)
		except:
			pass

		# updates openlayers3 images
		try:
			ndvi_lastimg(plotid=plotid)
		except:
			pass

		# weather forecast
		try:
			# ***ZOUBAIR*** : A supprimmer puisque c'est effectué plus haut dans weather_to_plot()
			satirr_weather_forecast(plotid)
		except:
			pass
		
		# Growing Degree Day
		try:
			satirr_GDD(plotid)
		except:
			pass

		# calculate kcb, fc and hydric budget
		ndvi_kcbfc(plotid=plotid)
		satirr_bilanhyd(plotid=plotid)	

	elif onlybilan == '100':
		try:
			connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
			con = psycopg2.connect(connString)
			cur = con.cursor()
			if plotid != '':
				sql="UPDATE satirr.couches SET initialiser_ndvi = 0 where idcouche="+str(plotid)
				cur.execute(sql)
				con.commit()
			sql="delete  from satirr.image where idcouche="+plotid
			cur.execute(sql)
			con.commit() 
		except psycopg2.Error as e:
			logging.error("Error %s", e)
			pass
		finally:
			if con:
				con.close()

		# intialize/update L8 NDVI 
		try:
			satirr_init_idL8(plotid=plotid)
		except:
			pass
		try:
			satirr_init_ndviL8(plotid=plotid)
		except:
			pass
	elif onlybilan == '200':
			satirr_weather_forecast(plotid)
	else :
		
		"""
		Cette opération doit être effectuée pour un changement paramètres de la parcelle.
		Dans ce cas, on actualise les uniquement le bilan hydrique
		"""	
			
		try:
			connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
			con = psycopg2.connect(connString)
			cur = con.cursor()
			if plotid != '':
				sql="UPDATE satirr.couches SET modis = 'Updating' where idcouche="+str(plotid)
				cur.execute(sql)
				con.commit()

			sql="delete from satirr.caracteristique where (type='kcb' or type='fc' or type like 'SWC' or type='ET' or type='irrigauto')and idcouche="+plotid
			cur.execute(sql)
			con.commit() 
		except psycopg2.Error as e:
			logging.error("Error %s", e)
			pass
		finally:
			if con:
				con.close()		
									
		# Growing Degree Day
		try:
			satirr_GDD(plotid)
		except:
			logging.error("Error GDD")
			pass
		# calculate kcb, fc and hydric budget
		ndvi_kcbfc(plotid)
		satirr_bilanhyd(plotid)	

	try:
		connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)	
		con = psycopg2.connect(connString)
		cur = con.cursor()
		if plotid != '':
			sql="UPDATE satirr.couches SET modis = '' where idcouche="+str(plotid)
			cur.execute(sql)
			con.commit()
	except psycopg2.Error as e:
	    logging.error("Error %s", e)
	    pass
	finally:
	    if con:
	        con.close()

	logging.info("done!")
					
if __name__ == '__main__':
	
	print(sys.argv)
	nbarg=sys.argv[1:].__len__()

	if nbarg == 0:
		# Pas d'argument: Actualisation de l'ensemble des parcelles
		satirr_main()

	elif nbarg == 1:
		# 1 argument : Actualisation d'une parcelle avec ndvi, meteo, GDD, bilan hydrique (argv[1]=plotid)
		print("ACTU ALL")
		satirr_actu(sys.argv[1],0)

	elif nbarg == 2:
		# 2argument : Actualisation du bilan hydrique d'une parcelle (argv[1]=plotid, argv[2]:bilan)
		print("ACTU ONLY BILAN")
		satirr_actu(sys.argv[1],sys.argv[2])	

