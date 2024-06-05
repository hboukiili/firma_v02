from django.shortcuts import render
import jwt.algorithms
import jwt.utils
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from models_only.models import Farmer
from .tools.ogimet import Ogimet_class
from rest_framework.permissions import IsAuthenticated
from .serializer import Ogimet_Serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from farmer.tools.FarmerAUTH import FARMERJWTAuthentication


class ogimet(APIView):
    
	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		operation_description="Create some data",
		request_body=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'Polygon': openapi.Schema(type=openapi.TYPE_STRING),
				'start_date': openapi.Schema(type=openapi.TYPE_STRING),
				'end_date' : openapi.Schema(type=openapi.TYPE_STRING)
			},
			required=['name']
		),
	)

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
		return Response ("Error in Input", status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):

		print(request.user.firstname, request.user.email)

		return Response("OK")