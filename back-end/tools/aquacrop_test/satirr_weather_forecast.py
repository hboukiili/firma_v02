# -*- coding: utf-8 -*-

"""

A collection of calls to weather forecast APIs:
    - openweather: http://api.openweathermap.org
    - wunderground: http://api.wunderground.com
    - forecast.io: https://api.forecast.io
    - yr.no

The routine also does an inverse geoloc and search for the elevation of the point (lat,lon) with mapquest

"""
import sys
sys.path.insert(0, '..')

import urllib
import simplejson as json
import logging
import datetime
import psycopg2
import ogr
import numpy as np
import pandas as pd


import config
from meteo_unit import *
from meteo_ET0 import Meteo_class


# https://github.com/wckd/python-yr et modifier 
# la ligne import json par import simplejson as json
# recopier le repertoir langage dans l'install
# installer la librairie xmltodict
#from yr.libyr import Yr 

# https://github.com/Rory-Sullivan/metno-locationforecast
import  metno_locationforecast as metno

"""

mapquest_geoloc(lat,lon)
call the Mapquest API of geocoding to retrieve the address of a point(lat,lon)

"""
def mapquest_geoloc(lat,lon):

    url="http://open.mapquestapi.com/geocoding/v1/reverse?key=Fmjtd%7Cluurn10720%2Ca0%3Do5-9wy05f&outFormat=json&callback=renderReverse&location="+str(lat)+","+str(lon)
    opener = urllib.request.build_opener()
    urllib.request.install_opener(opener)
    f = opener.open(url)
    json_string = f.read().decode()
    p = json.loads(str(json_string[14:json_string.__len__()-1]))
    pp=p['results'][0]['locations'][0]
    
    address=""
    if pp.__contains__('street'):address=address+pp['street']
    if pp.__contains__('adminArea5'):address=address+", "+pp['adminArea5']
    if pp.__contains__('adminArea3'):address=address+", "+pp['adminArea3']
    if pp.__contains__('adminArea1'):address=address+", "+pp['adminArea1']
    return(address)

"""

mapquest_elevation(lat,lon)
call the Mapquest API oto retrieve the elevation of a point(lat,lon)

"""
def mapquest_elevation(lat,lon):
   
    url="http://open.mapquestapi.com/elevation/v1/profile?key=Fmjtd|luurn10720%2Ca0%3Do5-9wy05f&shapeFormat=raw&latLngCollection="+str(lat)+","+str(lon)
    
    opener = urllib.request.build_opener()
    urllib.request.install_opener(opener)
    f = opener.open(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    masl=float(parsed_json['elevationProfile'][0]['height'])
    return(masl)

"""
Basic call and retrieving of openweather weather forecast

http://api.openweathermap.org/data/2.5/forecast/daily?lat=31.65&lon=-7.59&cnt=10&mode=json

"""

def openweather(lat,lon):
    APIkey='8c1b5ab9eb70be3638f6d7c685139a7c'
    url='http://api.openweathermap.org/data/2.5/forecast/daily?lat='+str(lat)+'&lon='+str(lon)+'&cnt=10&mode=json&APPID='+APIkey
    #print(url)
    
    f = f=urllib.request.urlopen(url) 
    json_string = f.read() 
    parsed_json = json.loads(json_string) 

    city=parsed_json['city']['name']
    city=city+','+parsed_json['city']['country']
    print('City: %s' % city)
    
    
    for day in range(10):
        t_min=parsed_json['list'][day]['temp']['min']-273.15
        t_max=parsed_json['list'][day]['temp']['max']-273.15
        hr_mean=parsed_json['list'][day]['humidity']
        pressure=parsed_json['list'][day]['pressure']
        clouds=parsed_json['list'][day]['clouds']
        wind_mean=parsed_json['list'][day]['speed']    
        
        print(day, t_min, t_max, hr_mean, pressure, clouds, wind_mean)

    f.close()

"""
Basic call and retrieving of wunderground weather forecast

http://api.wunderground.com/api/a3ddbe7815d31fa4/forecast10day/q/31.65,-7.59.json

"""
def wunderground(lat,lon):
    APIkey='a3ddbe7815d31fa4'
    url='http://api.wunderground.com/api/'+APIkey+'/forecast10day/q/'+str(lat)+','+str(lon)+'.json'
    #print(url)
    
    f = f=urllib.request.urlopen(url) 
    json_string = f.read() 
    parsed_json = json.loads(json_string) 

#    city=parsed_json['city']['name']
#    city=city+','+parsed_json['city']['country']
#    print('City: %s' % city)
    
    
    for day in range(10):
        t_min=float(parsed_json['forecast']['simpleforecast']['forecastday'][day]['low']['celsius'])
        t_max=float(parsed_json['forecast']['simpleforecast']['forecastday'][day]['high']['celsius'])
        hr_mean=float(parsed_json['forecast']['simpleforecast']['forecastday'][day]['avehumidity'])
        wind_mean=float(parsed_json['forecast']['simpleforecast']['forecastday'][day]['avewind']['kph'])/3.6    # km/hour-> meters/second
        rain_tot=float(parsed_json['forecast']['simpleforecast']['forecastday'][day]['qpf_allday']['mm'])
        cloud_condition=parsed_json['forecast']['simpleforecast']['forecastday'][day]['conditions']
        
        print(day, t_min, t_max, hr_mean, wind_mean, rain_tot, cloud_condition)

    f.close()

"""
Basic call and retrieving of forecast.io weather forecast

"""
# https://developer.forecast.io/docs/v2


def devforecast(lat,lon):
    APIkey='08d9171847be679007c92174a365a40f'
    url='https://api.forecast.io/forecast/'+APIkey+'/'+str(lat)+','+str(lon)+"?units=si"
    #print(url)
    
    f = f=urllib.request.urlopen(url) 
    json_string = f.read() 
    parsed_json = json.loads(json_string)     

    for day in range(8):
        t_min=float(parsed_json['daily']['data'][day]['temperatureMin'])    #celsius
        t_max=float(parsed_json['daily']['data'][day]['temperatureMax'])    # celsius
        hr_mean=float(parsed_json['daily']['data'][day]['humidity'])        # percent
        wind_mean=float(parsed_json['daily']['data'][day]['windSpeed'])     # meters/second
        dewPoint=float(parsed_json['daily']['data'][day]['dewPoint'])        # celsius
        cloudCover=float(parsed_json['daily']['data'][day]['cloudCover'])        
        precipProbability=float(parsed_json['daily']['data'][day]['precipProbability'])    
        precipIntensity=float(parsed_json['daily']['data'][day]['precipIntensity'])
        pressure=parsed_json['daily']['data'][day]['pressure']
        
        print(day, t_min, t_max, hr_mean, wind_mean, dewPoint, cloudCover,precipProbability,precipIntensity,pressure)

"""
weather_yrno(lat,lon,masl)
Weather Forecast from yr.no, daily resumes

input: latitude, longitude and elevation of point
output: now, dates, vals
    now1=[temperature,windDirection,windSpeed,humidity,pressure,cloudiness,dewpointTemperature]
    dates[]: table of dates in string 'yyyy-mm-dd'
    vals[*][11]: at bidimensional table with the output values:
        [prec_tot,temperature_avg,temperature_min, temperature_max,humidity_avg,humidity_min, humidity_max,windDirection_avg,windSpeed_avg,pressure_avg,cloudiness_avg,dewpointTemperature_avg])
    
"""

# def weather_yrno(lat,lon,masl):

#     try:
#         weather = Yr(coordinates=(lat,lon,int(masl)), language_name='en' )
        
#         # --- NOW ----
#         now1 = weather.now()
#         temperature=float(now1['location']['temperature']['@value'])
#         windDirection=float(now1['location']['windDirection']['@deg'])
#         windSpeed=float(now1['location']['windSpeed']['@mps'])
#         humidity=float(now1['location']['humidity']['@value'])
#         pressure=float(now1['location']['pressure']['@value'])
#         cloudiness=float(now1['location']['cloudiness']['@percent'])
#         dewpointTemperature=float(now1['location']['dewpointTemperature']['@value'])
        
#         logging.info("Temp:"+str(temperature)+" C\u00B0, Dew Point:"+str(dewpointTemperature)+" C\u00B0")
#         logging.info("WindSpeed:"+str(windSpeed)+" m/s, wind Direction:"+str(windDirection)+" \u00B0")
#         logging.info("Humidity:"+str(humidity)+" %, cloudiness:"+str(cloudiness)+" %, Pressure: "+str(pressure)+" hPa")
#         now1=[temperature,windDirection,windSpeed,humidity,pressure,cloudiness,dewpointTemperature]
        
#         # --- ForeCAST ----
#         forecast = weather.forecast(as_json=True)
    
#         dates=[]
#         vals=[]
#     #    dates=[""]*10
#     #    vals=np.zeros((10, 11), dtype='f')
        
#         dd=0
#         prec_tot=0
#         temperature_tot=0
#         windDirection_tot=0
#         windSpeed_tot=0
#         humidity_tot=0
#         pressure_tot=0
#         cloudiness_tot=0
#         dewpointTemperature_tot=0
#         temperature_min=100
#         temperature_max=-100
#         humidity_min=100
#         humidity_max=-100
#         compte=0
        
#         for forecast in weather.forecast():
#             #print(dd,"==>",forecast)
        
#             #forecast_from=forecast.get('@from')[0:10]
#             forecast_to=forecast.get('@to')[0:10]
        
#             if dd==0:forecast_to1=forecast_to
            
#             #print(forecast_to,forecast_to1)
        
#             if forecast_to!=forecast_to1:
#                 # ------ ET0 -----
#                 Tmean=temperature_tot/compte
#                 Tmin=temperature_min
#                 Tmax=temperature_max
#                 Rhmean=humidity_tot/compte
#                 Rhmin=humidity_min
#                 Rhmax=humidity_max
#                 uz=windSpeed_tot/compte
#                 h=10
#                 interior=1
#                 cloudiness=cloudiness_tot/compte
#                 Tdew=dewpointTemperature_tot/compte
#                 albedo=0.23
#                 rn=rs=n=ea=-9999

#                 aa=forecast_to1.split(sep='-')
#                 datepy=datetime.datetime(int(aa[0]),int(aa[1]),int(aa[2]))
#                 jday=int(datepy.strftime('%j'))
                    
#                 Et0=et0_pm(lat,jday,masl,rn,rs,n,ea,Tdew,Tmean,Tmin,Tmax,interior,Rhmin,Rhmax,Rhmean,uz,h,albedo,cloudiness)
            
#                 # --- stockage résultats ----
            
#                 dates.append(datepy)
#                 vals.append([prec_tot,Et0,Tmean,Tmin, Tmax,Rhmean,Rhmin, Rhmax,windDirection_tot/compte,uz,pressure_tot/compte,cloudiness,Tdew])
                                                        
#                 print("======== ",forecast_to1," ===========")
#                 print(forecast_to1,"Rain:",prec_tot)
#                 print(forecast_to1,"Temp:",temperature_tot/compte,temperature_min, temperature_max)
#                 print(forecast_to1,"Hum:",humidity_tot/compte,humidity_min, humidity_max)
#                 print(forecast_to1,"Wind:",windDirection_tot/compte,windSpeed_tot/compte)
#                 print(forecast_to1,"Other:",pressure_tot/compte,cloudiness_tot/compte,dewpointTemperature_tot/compte)
#                 print(forecast_to1,"ET0:",Et0)
    
#                 prec_tot=0
#                 temperature_tot=0
#                 windDirection_tot=0
#                 windSpeed_tot=0
#                 humidity_tot=0
#                 pressure_tot=0
#                 cloudiness_tot=0
#                 dewpointTemperature_tot=0
#                 temperature_min=100
#                 temperature_max=-100
#                 humidity_min=100
#                 humidity_max=-100
#                 compte=0
#                 forecast_to1=forecast_to
    
#             if forecast.__contains__('location') is True:
#                 forecast=forecast['location']
        
#                 if forecast.__contains__('precipitation') is True:
#                     precipitation=float(forecast['precipitation']['@value'])
#                     prec_tot+=precipitation
#                     #print('RAIN ',dd,forecast_from,forecast_to,"==>",precipitation)
#                 else:
#                     temperature=float(forecast['temperature']['@value'])
#                     windDirection=float(forecast['windDirection']['@deg'])
#                     windSpeed=float(forecast['windSpeed']['@mps'])
#                     humidity=float(forecast['humidity']['@value'])
#                     pressure=float(forecast['pressure']['@value'])
#                     cloudiness=float(forecast['cloudiness']['@percent'])
#                     dewpointTemperature=float(forecast['dewpointTemperature']['@value'])
        
#                     compte+=1
#                     temperature_tot+=temperature
#                     temperature_min=min(temperature_min,temperature)
#                     temperature_max=max(temperature_max,temperature)
#                     windDirection_tot+=windDirection
#                     windSpeed_tot+=windSpeed
#                     humidity_tot+=humidity
#                     humidity_min=min(humidity_min,humidity)
#                     humidity_max=max(humidity_max,humidity)
#                     pressure_tot+=pressure
#                     cloudiness_tot+=cloudiness
#                     dewpointTemperature_tot+=dewpointTemperature
#                     #print(dd,"==>",forecast_to,temperature,windDirection,windSpeed,humidity,pressure,cloudiness,dewpointTemperature)
    
#             dd=dd+1
#             #float(forecast['windSpeed']['@mps'])
#         return(now1,dates,vals)
#     except Exception as e:
#         print(e)
#         pass


def weather_api_met_no(lat,lon,masl):
    dates_out=[]
    vals_out=[]
    
    try:
        place = metno.Place("Myplace", lat, lon, masl)
        forecast = metno.Forecast(place, "Satirr michel.le_page@ird.fr")
        forecast.forecast_type='complete'
        forecast.update()
        
        table = np.zeros((len(forecast.data.intervals)-1,8))
        table_dates = []
        for i in range(len(forecast.data.intervals)-1):
            interval = forecast.data.intervals[i]

            table_dates.append(interval.start_time)

            table[i,0] = interval.variables["air_temperature"].value
            table[i,1]  = interval.variables["wind_from_direction"].value
            table[i,2]  = interval.variables["relative_humidity"].value
            table[i,3]  = interval.variables["air_pressure_at_sea_level"].value
            table[i,4]  = interval.variables["wind_speed"].value
            table[i,5]  = interval.variables["precipitation_amount"].value
            table[i,6]  = interval.variables["dew_point_temperature"].value
            table[i,7]  = interval.variables["cloud_area_fraction"].value
        data=pd.DataFrame(table)   
        dates=pd.DataFrame(table_dates)
        data.index = pd.to_datetime(dates[0])
        
        
        
        
        # 1er jour à 00:00
        ladate = datetime.datetime(data.index[0].year, data.index[0].month,data.index[0].day)
        
        while ladate < data.index[-1]:

            mask = (data.index>=ladate) & (data.index<ladate+datetime.timedelta(days=1))
            select=data.loc[mask]
            if select.index[0].hour ==0:
                # ------ ET0 -----
                Tmean = select[0].mean()
                Tmin = select[0].min()
                Tmax = select[0].max()
                Rhmean = select[2].mean()
                Rhmin = select[2].min()
                Rhmax = select[2].max()
                uz = select[4].mean()
                h=10
                interior=1
                cloudiness = select[7].mean()
                Tdew = select[6].mean()
                albedo=0.23
                rn=rs=n=ea=-9999
                
                jday=int(select.index[0].strftime('%j'))
                    
                Et0=Meteo_class().et0_pm(lat,jday,masl,rn,rs,n,ea,Tdew,Tmean,Tmin,Tmax,interior,Rhmin,Rhmax,Rhmean,uz,h,albedo,cloudiness)
                precip = select[5].sum()

                #print(select.index[0], Et0, Tmean, Tmax, Tmin, Rhmean, Rhmin, Rhmax, uz, Tdew, cloudiness, precip)
                dates_out.append(ladate)
                vals_out.append([precip, Et0, Tmean, Tmin, Tmax, Rhmean, Rhmin, Rhmax])
                

            ladate=ladate+datetime.timedelta(days=1)
        return(dates_out,vals_out,table_dates,table)
    except Exception as e:
        print(e)
        pass
            
def satirr_weather_forecast(plotid=''):

    logging.basicConfig(format = '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',level=config.debug,datefmt='%m-%d %H:%M')
    logging.info("===================== SATIRR WEATHER FORECAST ==============================")


    try:
        # connexion psycopg2
        connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)    
        con = psycopg2.connect(connString)
        cur = con.cursor()
        
        # look for the path/row of each plot based on its centroid
        connString2 = "PG: host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)    
        if plotid=="":
            sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where  date is not NULL and to_date(date,'YYYY-MM-DD') >= now() - interval '1 year'"
        else:
            sql="select ST_AsText(ST_centroid(geometry)),idcouche,date from satirr.couches  where  date is not NULL and to_date(date,'YYYY-MM-DD') >= now() - interval '1 year'  and idcouche="+str(plotid)

        conn = ogr.Open(connString2)
        layer = conn.ExecuteSQL(sql)
    
        feat = layer.GetNextFeature()
        
        while feat is not None:
            idcouche=feat.GetField('idcouche')
            # on a demandé le centroide à postgis: on cherche la station WMO la plus proche et on l'introduit dans la BD
            geom=feat.GetGeometryRef()
            lon=geom.GetPoint(0)[0]
            lat=geom.GetPoint(0)[1]
            print(lon,lat)

            address=mapquest_geoloc(lat,lon)
            print(address)
            
            masl=mapquest_elevation(lat,lon)
            print("Latitude=",lat,", Longitude=",lon," ,Elevation=",masl," masl")
            
            logging.info("------- YR.NO -------")
            dates,vals,dates_h,vals_h=weather_api_met_no(lat,lon,masl)        
            
            # introduction des données horraire dans satirr.forecast
            if vals_h.__len__()>0:

                try:

                    for i in range(len(dates_h)):
                        ladate=dates_h[i].strftime('%Y-%m-%d %H:%M:%S')
                        tair=vals_h[i][0]
                        Dv=vals_h[i][1]
                        HR=vals_h[i][2]
                        Pair=vals_h[i][3]
                        Vv=vals_h[i][4]
                        fpluie=vals_h[i][5]
                        Tdew=vals_h[i][6]
                        Cfr=vals_h[i][7]

                        if fpluie<0:
                            fpluie=0


                        #sql = 'delete from satirr.caracteristique where idcouche='+str(idcouche)+" and date='"+ladate+"' and (type='pluie' or type='tmin' or type='tmax' or type='tmean') and (id_source=102);"

                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'pluie\',' + str(fpluie)
                        sql = 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(fpluie))+";"
                        
                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'tair\',' + str(tair)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(tair))+";"
                        
                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'dv\',' + str(Dv)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(Dv))+";"

                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'hr\',' + str(HR)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(HR))+";"

                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'pair\',' + str(Pair)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(Pair))+";"

                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'vv\',' + str(Vv)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(Vv))+";"

                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'tdew\',' + str(Tdew)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(Tdew))+";"

                        values = str(idcouche) + ',\'NO\',' + '\'' + ladate + '\'' + ',\'cloud\',' + str(Cfr)
                        sql = sql + 'insert into satirr.forecast (idcouche, provider, date, type, valeur) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab_forecast DO UPDATE SET valeur = "+str("%f"%(Cfr))+";"
                        
                        logging.debug(" ====>  %s",sql)
                        cur.execute(sql)
                        con.commit()     
                        
                except (OSError, IOError) as e:
                    print(e.args)
                    pass
        
            feat.Destroy()
            feat = layer.GetNextFeature()
            
            
            
        while feat is not None:
            idcouche=feat.GetField('idcouche')
            # on a demandé le centroide à postgis: on cherche la station WMO la plus proche et on l'introduit dans la BD
            geom=feat.GetGeometryRef()
            lon=geom.GetPoint(0)[0]
            lat=geom.GetPoint(0)[1]
            print(lon,lat)

            address=mapquest_geoloc(lat,lon)
            print(address)
            
            masl=mapquest_elevation(lat,lon)
            print("Latitude=",lat,", Longitude=",lon," ,Elevation=",masl," masl")
            
            logging.info("------- YR.NO -------")
            dates,vals,dates_h,vals_h=weather_api_met_no(lat,lon,masl)       
            
            
            # introduction des données journalières dans satirr.caracteristique
            if vals.__len__()>0:

                try:

                    for i in range(len(dates)):
                        ladate=dates[i].strftime('%Y-%m-%d')
                        fET0=vals[i][1]
                        fpluie=vals[i][0]
                        tmin=vals[i][3]
                        tmax=vals[i][4]
                        tmean=vals[i][2]

                        if fpluie<0:
                            fpluie=0


                        #sql = 'delete from satirr.caracteristique where idcouche='+str(idcouche)+" and date='"+ladate+"' and (type='pluie' or type='tmin' or type='tmax' or type='tmean') and (id_source=102);"

                        values = str(idcouche) + ',\'pluie\',' + str(fpluie) + ',\'' + ladate + '\'' + ',0,    102'
                        sql = 'insert into satirr.caracteristique (idcouche, type, valeur,date,interpoler,id_source) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab DO UPDATE SET valeur = "+str("%f"%(fpluie))+";"
                        
                        values = str(idcouche) + ',\'tmin\',' + str(tmin) + ',\'' + ladate + '\'' + ',0,    102'
                        sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,interpoler,id_source) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab DO UPDATE SET valeur = "+str("%f"%(tmin))+";"
                        
                        values = str(idcouche) + ',\'tmax\',' + str(tmax) + ',\'' + ladate + '\'' + ',0,    102'
                        sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,interpoler,id_source) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab DO UPDATE SET valeur = "+str("%f"%(tmax))+";"
                        
                        values = str(idcouche) + ',\'tmean\',' + str(tmean) + ',\'' + ladate + '\'' + ',0,    102'
                        sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,interpoler,id_source) VALUES (' + values + ')'\
                            +" ON CONFLICT ON CONSTRAINT uc_tab DO UPDATE SET valeur = "+str("%f"%(tmean))+";"
                            
                        if fET0>=0 and fET0<12: 
                            #sql = sql + 'delete from satirr.caracteristique where idcouche='+str(idcouche)+" and date='"+ladate+"' and (type='ET0') and (id_source=    102);"

                            values = str(idcouche) + ',\'ET0\',' + str(fET0) + ',\'' + ladate + '\'' + ',0,    102'
                            sql = sql + 'insert into satirr.caracteristique (idcouche, type, valeur,date,interpoler,id_source) VALUES (' + values + ')'\
                                +" ON CONFLICT ON CONSTRAINT uc_tab DO UPDATE SET valeur = "+str("%f"%(fET0))+";"
                        
                        logging.debug(" ====>  %s",sql)
                        cur.execute(sql)
                        con.commit()     
                        
                except (OSError, IOError) as e:
                    print(e.args)
                    pass
        
            feat.Destroy()
            feat = layer.GetNextFeature()
                    
    except psycopg2.Error as e:
        logging.error("Error %s", e)
        pass
        
        
    finally:
        
        if conn:  conn.Destroy()
        if con:  con.close()    

                                    
if __name__ == "__main__": 
    
    connString = "host=%s dbname=%s user=%s password=%s" %(config.databaseServer,config.databaseName,config.databaseUser,config.databasePW)    
    con = psycopg2.connect(connString)
    cur = con.cursor()

    sql = ("select idcouche from satirr.couches cs")
    cur.execute(sql)
    ver = cur.fetchall()
    for i in range(len(ver)):
        Parcelle_id=ver[i]
        Parcelle_id=Parcelle_id[0]
        satirr_weather_forecast(Parcelle_id)
    
 