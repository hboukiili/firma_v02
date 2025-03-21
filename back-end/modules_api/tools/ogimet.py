import datetime
import os
import psycopg2
import json
import numpy as np
import urllib.request
import time
import logging
from models_only.models import Ogimet_stations
# from math import radians, sin, cos, sqrt, atan2
from math import *


class Ogimet_class:

    def __init__(self):
        self.version = "1.0"
        self.url = "http://www.ogimet.com/cgi-bin/getsynop"
        # self.capteurs = {
        #                     1:{"nom":"rainfall sensor (unknown)", "reference":"9999", "hauteur":"2"},
        #                     2:{"nom":"temperature sensor (unknown)", "reference":"9999", "hauteur":"2"},
        #                     3:{"nom":"visibility sensor (unknown)", "reference":"9999", "hauteur":"2"},
        #                     4:{"nom":"weathercock (unknown)", "reference":"9999", "hauteur":"2"},
        #                     5:{"nom":"anemometer (unknown)", "reference":"9999", "hauteur":"2"},
        #                     6:{"nom":"dew temperature sensor (unknown)", "reference":"9999", "hauteur":"2"},
        #                     7:{"nom":"pressure sensor (unknown)", "reference":"9999", "hauteur":"2"}
                        # }
        # self.variables={
        #                 "Rainfall":{"description":"Precipitation", "unite":"mm", "minimum":"0", "maximum":"200"},
        #                 "Temperature":{"description":"Air Temperature", "unite":"C", "minimum":"-10", "maximum":"50"},
        #                 "Visibility":{"description":"Visibility", "unite":"km", "minimum":"0", "maximum":"100"},
        #                 "WinDir":{"description":"Wind Direction", "unite":"deg", "minimum":"0", "maximum":"360"},
        #                 "WindSpeed":{"description":"Wind Speed", "unite":"m.s-1", "minimum":"0", "maximum":"100"},
        #                 "Tdew":{"description":"Dew Temperature", "unite":"C", "minimum":"-100", "maximum":"100"},
        #                 "Pressure":{"description":"Air Pressure", "unite":"mb", "minimum":"0", "maximum":"2000"}           
        #             }
        self.id = ""
        self.location_name = ""
        self.data = ""

        
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
        closest_stations = [{'station_id': station.station_id, 'location_name': station.location_name} for station, _ in sorted_stations]
        return closest_stations
    

    def parse_visibility(self, visi, aqua):
        if visi[3:5] == '//':
            # if aqua == 1:
                return -9999
            # return np.nan
        if visi[-1] != '/':
            visibility = float(visi[3:5])
        else:
            visibility = float(visi[2:4])
        if visibility < 50:
            return visibility / 10
        elif visibility < 90:
            return visibility - 50
        else:
            # if aqua == 0:
            #     return {
            #         '91': 0.05,
            #         '92': 0.2,
            #         '93': 0.5,
            #         '94': 1.,
            #         '95': 2.,
            #         '96': 4.,
            #         '97': 10.,
            #         '98': 20.,
            #         '99': 50.
            #     }.get(visi[3:5], np.nan)
            return {
                    '91': 0.05,
                    '92': 0.2,
                    '93': 0.5,
                    '94': 1.,
                    '95': 2.,
                    '96': 4.,
                    '97': 10.,
                    '98': 20.,
                    '99': 50.
                }.get(visi[3:5], -9999)

    def decode_data_for_aquacrop(self):
            
        Rainfall_list, Visibility_list, Temperature_list, WinDir_list, WindSpeed_list, Tdew_list, Pressure_list  = {}, {}, {}, {}, {}, {}, {}

        for Lig in self.data:
            
            L = str(Lig).replace("b'", '').split(" ")
            data1 = L[0].split(',') 
            Rainf = np.nan
            Rainf_timeacc = -9999

            if len(L) > 4:
                if data1[0] == self.id and L[3] != 'NIL=':
                    Tmean = Rainf = Tdew = P  = -9999
                    Uz = np,nan
                    Visibility = np.nan
                    Tmean = np.nan
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
                    codeRain = L[3][0]
                    if codeRain == '4':
                        Rainf = 0.
                    elif codeRain=='5':
                        Rainf = -9999
                    visi=L[3]

                    Visibility = self.parse_visibility(visi, 0)
                    
                    

                    if L[4][1:3] != '//':
                        dv1=float(L[4][1:3])
                        dv=dv1 * 10
                    else :
                        dv = -9999
                    if L[4][3:5] != '//':
                        Uz=float(L[4][3:5])
                        Uz=Uz*MultWind
                    else :
                        Uz = -9999
                    
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
                                # print(str(annee+'-'+mois+'-'+jour+','+heure+'-'+minute)," L[i]:",L[i])
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
                                # print('===> SECTION 1 code 6 ',L[i],Rainf, Rainf_timeacc)
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
                                    # print("===> SECTION 2 code 6", Rainf_S2, Rainf_S2_timeacc )
                            elif code=='7': # Precipitation in mm for 24h
                                Rainf_S2=float(L[i][1:5])
                                if Rainf_S2>=900 and Rainf_S2<990: Rainf_S2=(Rainf_S2-990)/10.
                                elif Rainf_S2>=990: Rainf_S2=(Rainf_S2-990)/10.
                                else: Rainf_S2=Rainf_S2/10.

                                if Rainf_S2==900.90: Rainf_S2=0

                                Rainf_S2_timeacc = 24
                                # print("===> SECTION 2 code 7", Rainf_S2, Rainf_S2_timeacc )

                    date = datetime.datetime(int(annee),int(mois),int(jour)).strftime("%Y-%m-%d")
                    
                    if date not in Temperature_list:
                        
                        Temperature_list[date] = []
                        WindSpeed_list[date] = []
                        Rainfall_list[date] = []
                        Tdew_list[date] = []
                        Visibility_list[date] = []
                    
                    Temperature_list[date].append(Tmean)
                    WindSpeed_list[date].append(Uz)
                    Tdew_list[date].append(Tdew)
                    Visibility_list[date].append(Visibility)
                    Rainfall_list[date].append(Rainf)

        return Temperature_list, WindSpeed_list, Tdew_list, Rainfall_list, Visibility_list

    def Extraterrestrial_radiation(self, lat,jday):
        lat_rad=lat*pi/180.
        dr=1 + 0.033 * cos(2*pi/365*jday)
        soldecl=0.409*sin((2*pi/365*jday) - 1.39)
        sunset_angle=acos(-tan(lat_rad)*tan(soldecl))
        
        ra= (24*60/pi)* 0.082 * dr * (sunset_angle * sin(lat_rad) * sin(soldecl) + cos(lat_rad) * cos(soldecl) * sin(sunset_angle))

        return(ra)

    def Solar_radiation_cloudiness(self, lat,jday,cF):

        const_as = 0.25
        const_bs = 0.5
        ra = self.Extraterrestrial_radiation(lat,jday)
        rs = (const_as+const_bs*cF/100.)*ra
        return(rs)


    def decode_data(self):
        
        Rainfall_list, Visibility_list, Temperature_list, WinDir_list, WindSpeed_list, Tdew_list, Pressure_list  = [], [], [], [], [], [], []
        for Lig in self.data:
            
            L = str(Lig).replace("b'", '').split(" ")
            
            data1 = L[0].split(',')
            Rainf = -9999
            Rainf_timeacc = -9999
            if len(L) > 4:
                if data1[0] == self.id and L[3] != 'NIL=':
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
                    # print('L[3] = ', L[3])
                    visi=L[3]

                    Visibility = self.parse_visibility(visi, 1)
                    
                    

                    if L[4][1:3] != '//':
                        dv1=float(L[4][1:3])
                        dv=dv1 * 10
                    else :
                        dv = -9999
                    if L[4][3:5] != '//':
                        Uz=float(L[4][3:5])
                        Uz=Uz*MultWind
                    else :
                        Uz = -9999
                    
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
                                # print(str(annee+'-'+mois+'-'+jour+','+heure+'-'+minute)," L[i]:",L[i])
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
                                # print('===> SECTION 1 code 6 ',L[i],Rainf, Rainf_timeacc)
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
                                    # print("===> SECTION 2 code 6", Rainf_S2, Rainf_S2_timeacc )
                            elif code=='7': # Precipitation in mm for 24h
                                Rainf_S2=float(L[i][1:5])
                                if Rainf_S2>=900 and Rainf_S2<990: Rainf_S2=(Rainf_S2-990)/10.
                                elif Rainf_S2>=990: Rainf_S2=(Rainf_S2-990)/10.
                                else: Rainf_S2=Rainf_S2/10.

                                if Rainf_S2==900.90: Rainf_S2=0

                                Rainf_S2_timeacc = 24
                                # print("===> SECTION 2 code 7", Rainf_S2, Rainf_S2_timeacc )

                    date = datetime.datetime(int(annee),int(mois),int(jour), int(heure), int(minute))

                    timestamp = datetime.datetime.timestamp(date)
                    timestamp = int(timestamp)
                    
                    Rainfall_list.append([timestamp, Rainf])
                    Temperature_list.append([timestamp, Tmean])
                    Visibility_list.append([timestamp, Visibility])
                    WinDir_list.append([timestamp, dv])
                    WindSpeed_list.append([timestamp, Uz])
                    Tdew_list.append([timestamp, Tdew])
                    Pressure_list.append([timestamp, P])

        final_data = {
            "station" : self.location_name,
            "Rainfall mm" : Rainfall_list,
            "Temperature C" : Temperature_list,
            "Visibility Km" : Visibility_list,
            "WinDir deg" : WinDir_list,
            "WindSpeed m.s-1" : WindSpeed_list,
            "Tdew C" : Tdew_list,
            "Pressure mb" : Pressure_list
        }
                    

        return final_data
        
    def download(self, stations, date_begin, date_end):
        
        date_end_format = datetime.datetime.strptime(date_end,'%Y-%m-%d').strftime("%Y%m%d%H%M")    
        date_begin_format = datetime.datetime.strptime(date_begin,'%Y-%m-%d').strftime("%Y%m%d%H%M")
        
        for station in stations:
            id = str(station["station_id"])
            pause = 0

            # params = {
            #     'block': id,
            #     'begin': date_begin_format,
            #     'end': date_end_format
            # }

            while pause <= 60:
                try:
                    response =urllib.request.urlopen(self.url+"?block="+id+"&begin="+date_begin_format+"&end="+date_end_format+"")
                    response_body = response.readlines()
                except urllib.error.URLError as e:
                    return -1
                # print(len(response_body))
                if response.status == 501:
                    
                    pause += 30
                    time.sleep(pause)
                    
                else:
                    self.data =  response_body
                    self.id =  id
                    self.location_name = station["location_name"]
                    return True

        return False


if __name__ == '__main__':

    Ogimet = Ogimet_class()
    
    stations = Ogimet.get_closest_stations(34.33597054747763, -4.885676122165933)
    # print(stations)
    # data = Ogimet.download( 60060, "2018-01-01", "2018-05-05" )
    # print(ogimet_file)