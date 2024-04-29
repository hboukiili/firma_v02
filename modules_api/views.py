from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response 
from models_only.models import Agriculture
from .tools.ogimet import Ogimet_class
# Create your views here.

class ogimet(APIView):
    
    def get(self, request):
        
        Ogimet = Ogimet_class()
    
        stations_ids = Ogimet.get_closest_stations(34.33597054747763, -4.885676122165933)
        data, station_id = Ogimet.download(stations_ids, "2018-01-01", "2018-01-05")
        decoded_data = Ogimet.decode_data(station_id, data)
        return Response (decoded_data)
