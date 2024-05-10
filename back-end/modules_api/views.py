from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from models_only.models import Agriculture
from .tools.ogimet import Ogimet_class
from rest_framework.permissions import IsAuthenticated
from .serializer import Ogimet_Serializer

class ogimet(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = Ogimet_Serializer(data=request.data)

        if serializer.is_valid() :
    
            Ogimet = Ogimet_class()

            Polygon = serializer.validated_data.get("Polygon")
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')

            stations_ids = Ogimet.get_closest_stations(32.04071866778945, -7.700995879688435)
            result = Ogimet.download(stations_ids, "2018-01-01", "2018-01-05")
            if result:
                decoded_data = Ogimet.decode_data()
                return Response (decoded_data, status=status.HTTP_200_OK)
            return Response ("No Data Has been found", status=status.HTTP_404_NOT_FOUND)
        return Response ("Error in Input", status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def get(self, request):

        return Response("OK")