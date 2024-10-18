from django.shortcuts import render
import jwt.algorithms
import jwt.utils
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from models_only.models import Farmer, Field
from .tools.ogimet import Ogimet_class
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import Ogimet_Serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from farmer.tools.FarmerAUTH import FARMERJWTAuthentication
from .tools.aquacrop_ import aquacrop_run
from  datetime import datetime, timedelta
from .tools.gee import aquacrop_
from .tools.Open_meteo import Open_meteo

class ogimet(APIView):
    
	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		request_body=Ogimet_Serializer,
		responses={201: Ogimet_Serializer}
	)

	def post(self, request):

		
		serializer = Ogimet_Serializer(data=request.data)

		if serializer.is_valid() :

			Ogimet = Ogimet_class()

			field_id = serializer.validated_data.get("field_id")
			start_date = serializer.validated_data.get('start_date')
			end_date = serializer.validated_data.get('end_date')

			try :
	
				field = Field.objects.get(id=field_id)
				point = field.boundaries[0][0]
				stations_ids = Ogimet.get_closest_stations(point[1], point[0])
				result = Ogimet.download(stations_ids, start_date, end_date)
				if result:
					decoded_data = Ogimet.decode_data()
					return Response (decoded_data, status=status.HTTP_200_OK)
				return Response ("No Data Has been found", status=status.HTTP_404_NOT_FOUND)
					
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):

		print(request.user.firstname, request.user.email)

		return Response("OK")
	
class aquacrop(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]


	def get(self, request):

		return Response(aquacrop_run())

	@swagger_auto_schema(
		request_body=Ogimet_Serializer,
		responses={201: Ogimet_Serializer}
	)

	
	def post(self, request):

		serializer = Ogimet_Serializer(data=request.data)
		user = request.user
		
		if serializer.is_valid() :

			# Ogimet = Ogimet_class()
			field_id = serializer.validated_data.get("field_id")
			start_date = serializer.validated_data.get('start_date')
			end_date = serializer.validated_data.get('end_date')

			try :

				field = Field.objects.get(id=field_id)
				point = field.boundaries[0][0]
				weather = Open_meteo(start_date,end_date,point[1], point[0])
				# stations_ids = Ogimet.get_closest_stations(point[1], point[0])
# 				result = Ogimet.download(stations_ids, start_date, end_date)
# 				if result:
# 					T, Ws, Tdew, Rain, Visibility = Ogimet.decode_data_for_aquacrop()
				result = aquacrop_run(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d'), weather, point[0], point[1])
				return Response (result, status=status.HTTP_200_OK)
				# return Response ("No Data Has been found", status=status.HTTP_404_NOT_FOUND)
						
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class gee(APIView):

	pass
