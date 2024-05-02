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
    
        stations_ids = Ogimet.get_closest_stations(32.04071866778945, -7.700995879688435)
        result = Ogimet.download(stations_ids, "2018-01-01", "2018-01-05")
        if result:
            decoded_data = Ogimet.decode_data()
        return Response (decoded_data)
