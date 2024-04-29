import datetime
import os
import psycopg2
import json
import numpy as np
import urllib.request
import time
import logging
from models_only.models import Ogimet_stations
from math import radians, sin, cos, sqrt, atan2


class Ogimet_class:

    def __init__(self):
        self.version = "1.0"
        self.url = "http://www.ogimet.com/cgi-bin/getsynop"
        self.capteurs = {
                            1:{"nom":"rainfall sensor (unknown)", "reference":"9999", "hauteur":"2"},
                            2:{"nom":"temperature sensor (unknown)", "reference":"9999", "hauteur":"2"},
                            3:{"nom":"visibility sensor (unknown)", "reference":"9999", "hauteur":"2"},
                            4:{"nom":"weathercock (unknown)", "reference":"9999", "hauteur":"2"},
                            5:{"nom":"anemometer (unknown)", "reference":"9999", "hauteur":"2"},
                            6:{"nom":"dew temperature sensor (unknown)", "reference":"9999", "hauteur":"2"},
                            7:{"nom":"pressure sensor (unknown)", "reference":"9999", "hauteur":"2"}
                        }
        self.variables={
                        1:{"nom":"Rainfall", "description":"Precipitation", "unite":"mm", "minimum":"0", "maximum":"200"},
                        2:{"nom":"Temperature", "description":"Air Temperature", "unite":"C", "minimum":"-10", "maximum":"50"},
                        3:{"nom":"Visibility", "description":"Visibility", "unite":"km", "minimum":"0", "maximum":"100"},
                        4:{"nom":"WinDir", "description":"Wind Direction", "unite":"deg", "minimum":"0", "maximum":"360"},
                        5:{"nom":"WindSpeed", "description":"Wind Speed", "unite":"m.s-1", "minimum":"0", "maximum":"100"},
                        6:{"nom":"Tdew", "description":"Dew Temperature", "unite":"C", "minimum":"-100", "maximum":"100"},
                        7:{"nom":"Pressure", "description":"Air Pressure", "unite":"mb", "minimum":"0", "maximum":"2000"}           
                    }     

        
    def haversine(self, lat1, lon1, lat2, lon2):
        
        """
        Calculate the distance between two points on the Earth's surface using the Haversine formula.
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        # Radius of the Earth in kilometers
        radius = 6371
        distance = radius * c
        return distance
        
    def get_closest_stations(self, user_lat, user_lon, num_stations=5):
        """
        Get the closest stations to a given latitude and longitude.
        """
        # Query all stations from the database
        stations = Ogimet_stations.objects.all()
        
        # Calculate the distance to each station and store it in a dictionary
        distances = {}
        for station in stations:
            distance = self.haversine(float(user_lat), float(user_lon), float(station.lat), float(station.long))
            distances[station] = distance
        
        # Sort the stations by distance and get the 5 closest ones
        sorted_stations = sorted(distances.items(), key=lambda x: x[1])[:num_stations]
        closest_stations = [station.station_id for station, _ in sorted_stations]    
        return closest_stations
    
    def decode_data(self, id_station, data):
        
        Ligs = str(data)
        Ligs = Ligs.split('\\n')
        final_data = []

        for Lig in Ligs:
            
            L = Lig.split(" ")
            
            data1 = L[0].split(',')
            Rainf = -9999
            Rainf_timeacc = -9999
            
            if len(L) > 4:
                
                if data1[0] == id_station and L[3] != 'NIL=':
                    Tmean=Rainf=Tdew=Visibility=P=Uz= -9999
                    annee = data1[1]
                    mois = data1[2]
                    jour = data1[3]
                    heure = data1[4]
                    minute = data1[5]
                    
                    codewind=L[1][4]
                    MultWind = {
                                '0': 1.,
                                '1': 1.,
                                '2': 0.5144,
                                '3': 0.5144    ,
                                '4': 0.5144                                
                                }[codewind]
                    codeRain=L[3][0]
                    if codeRain=='4':
                        Rainf=0.
                    elif codeRain=='5':
                        Rainf= -9999
                    visi=L[3]

                    if(visi[3:5]=='//'):
                        Visibility = -9999
                    
                    else:
                        
                        Visibility = float(visi[3:5])
                        if Visibility < 50:
                            Visibility / 10.
                        elif Visibility < 90:
                            Visibility = Visibility-50
                        else:
                            Visibility = {
                                '91': 0.05,
                                '92': 0.2,
                                '93': 0.5,
                                '94': 1.,
                                '95': 2.,
                                '96': 4.,
                                '97': 10.,
                                '98': 20.,
                                '99': 50.                                    
                                }[visi[3:5]]

                    dv1=float(L[4][1:3])
                    dv=dv1 * 10
                    
                    Uz=float(L[4][3:5])
                    Uz=Uz*MultWind
                    
                    i=5
                
                    section=1
                    
                    for i in range(5,L.__len__()):

                        if L[i]=='333': section = 2
                        if L[i]=='222': section = 9
                    
                        if section == 1:
                            code=L[i][0]
                            if code=='1': # Temperature
                                Tmean = float(L[i][2:5]) / 10.
                                
                                if L[i][1] == 1: Tmean =- Tmean
                        
                            elif code=='2': # Dewpoint
                                Tdew=float(L[i][2:5])/10.
                                if L[i][1]==1: Tdew=-Tdew

                            elif code=='3': # Station pressure in 0.1 mb
                                P=float(L[i][2:5])*10.
                            
                            #elif code=='5': # Pressure
                            #    tendanceP=int(L[i][0:1])
                            #    hpression=float(L[i][2:5])/10.
                            
                            elif code=='6': # Precipitation in mm
                                print(str(annee+'-'+mois+'-'+jour+','+heure+'-'+minute)," L[i]:",L[i])
                                Rainf=float(L[i][1:4])
                                if Rainf>=900 and Rainf<989: Rainf=0.
                                elif Rainf>=990: Rainf=(Rainf-990)/10.
                                
                                Rainf_timeacc = {
                                    '0': 6,
                                    '1': 6,
                                    '2': 12,
                                    '3': 18,
                                    '4': 24,
                                    '5': 1,
                                    '6': 2,
                                    '7': 3,
                                    '8': 9,
                                    '9': 15,
                                    '/': 24
                                    }[L[i][4:5]]                                
                                print('===> SECTION 1 code 6 ',L[i],Rainf, Rainf_timeacc)
                            elif code=='/' or code=='7': # fin
                                break

                        elif section==2:
                            code=L[i][0]
                            if code=='6': # Precipitation in mm for 24h
                                if [L[i][4:5]]=='4':
                                    Rainf_S2=float(L[i][1:4])
                                    if Rainf_S2>=900 and Rainf_S2<989: Rainf_S2=0.
                                    elif Rainf_S2>=990: Rainf_S2=(Rainf_S2-990)/10.
                                    else: Rainf_S2=Rainf_S2/10.

                                    if Rainf_S2==900.90: Rainf_S2=0

                                    Rainf_S2_timeacc = 24
                                    print("===> SECTION 2 code 6", Rainf_S2, Rainf_S2_timeacc )
                            elif code=='7': # Precipitation in mm for 24h
                                Rainf_S2=float(L[i][1:5])
                                if Rainf_S2>=900 and Rainf_S2<990: Rainf_S2=(Rainf_S2-990)/10.
                                elif Rainf_S2>=990: Rainf_S2=(Rainf_S2-990)/10.
                                else: Rainf_S2=Rainf_S2/10.

                                if Rainf_S2==900.90: Rainf_S2=0

                                Rainf_S2_timeacc = 24
                                print("===> SECTION 2 code 7", Rainf_S2, Rainf_S2_timeacc )

                    date = datetime.datetime(int(annee),int(mois),int(jour))
                    
                    final_data.append({
                        "date" : date.strftime('%Y-%m-%d'),
                        "hour" : f"{heure}:{minute}",
                        "Rainfall" : Rainf,
                        "Temperature" : Tmean,
                        "Visibility" : Visibility,
                        "WinDir" : dv,
                        "WindSpeed" : Uz,
                        "Tdew" : Tdew,
                        "Pressure" : P
                    })

        return final_data
        
    def download(self, id_station, date_begin, date_end):

        date_end_format = datetime.datetime.strptime(date_end,'%Y-%m-%d').strftime("%Y%m%d%H%M")    
        date_begin_format = datetime.datetime.strptime(date_begin,'%Y-%m-%d').strftime("%Y%m%d%H%M")
        
        for id in id_station:
            id = str(id)
            pause = 0
            while pause <= 60:
                try:
                    response =urllib.request.urlopen(self.url+"?block="+id+"&begin="+date_begin_format+"&end="+date_end_format+"")
                except urllib.error.URLError as e:
                    return -1
                
                if response.status == 501:
                    
                    pause += 30
                    time.sleep(pause)
        
                else :
                    return response.read(), id
        return -1


if __name__ == '__main__':

    Ogimet = Ogimet_class()
    
    stations = Ogimet.get_closest_stations(34.33597054747763, -4.885676122165933)
    print(stations)
    # data = Ogimet.download( 60060, "2018-01-01", "2018-05-05" )
    # print(ogimet_file)