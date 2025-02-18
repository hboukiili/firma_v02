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
from .tools.Open_meteo import fao_Open_meteo
import os
import rasterio
import numpy as np
import requests
import matplotlib.pyplot as plt
import logging
from .tools.weather import *


logger = logging.getLogger(__name__)

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
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error	
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
			user = request.user
			field_id = serializer.validated_data.get("field_id")
			start_date = serializer.validated_data.get('start_date')
			end_date = serializer.validated_data.get('end_date')

			try :

				field = Field.objects.get(id=field_id, user_id=user.id)
				point = field.boundaries[0][0]
				weather = fao_Open_meteo(start_date,end_date,point[1], point[0])
				# stations_ids = Ogimet.get_closest_stations(point[1], point[0])
# 				result = Ogimet.download(stations_ids, start_date, end_date)
# 				if result:
# 					T, Ws, Tdew, Rain, Visibility = Ogimet.decode_data_for_aquacrop()
				result = aquacrop_run(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d'), weather, point[0], point[1])
				return Response (result, status=status.HTTP_200_OK)
				# return Response ("No Data Has been found", status=status.HTTP_404_NOT_FOUND)
						
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error	
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FaoTest(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		field_id = request.query_params.get('field_id')
		if not field_id:
			return Response({"error": "Field ID is required."}, status=status.HTTP_400_BAD_REQUEST)
		
		path = f"/app/Data/fao_output/{field_id}"
		if not os.path.exists(path):
			return Response({"error": f"Path {path} does not exist."}, status=status.HTTP_404_NOT_FOUND)
		
		folders = os.listdir(path)
		if not folders:
			return Response({"error": f"No data found for Field ID: {field_id}."}, status=status.HTTP_404_NOT_FOUND)
		
		final_data = {}
		dates = []

		try:
			for folder in folders:
				min_values, max_values, mean_values = [], [], []
				folder_path = os.path.join(path, folder)
				files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.tif')]
				files = sorted(files, key=lambda x: x.split('.')[0])

				if not dates:
					dates = [file.split('.')[0].split('_')[1] for file in files]

				for file in files:
					file_path = os.path.join(folder_path, file)
					with rasterio.open(file_path) as src:
						data = src.read(1)
						mean_value = np.nanmean(data)
						min_value = np.nanmin(data)
						max_value = np.nanmax(data)
						min_values.append(min_value)
						mean_values.append(mean_value)
						max_values.append(max_value)

				final_data[folder] = {
					'min': min_values,
					'max': max_values,
					'mean': mean_values
				}

			final_data['dates'] = dates
			print(final_data['rzsm_pr'])
			return Response(final_data, status=status.HTTP_200_OK)

		except Exception as e:
			logger.error(f"Error processing field_id {field_id}: {str(e)}")
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class current_weather(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):

		field_id = request.query_params.get('field_id')

		if field_id != None:

			try :
				user = request.user
				API_key = "85461dddb7698ac03b2bf4c5b22f5369"
				field = Field.objects.get(id=field_id, user_id=user.id)
				point = field.boundaries[0][0]
				lat = point[1]
				lon = point[0]
				params = {
					"lat": lat,           
					"lon": lon,         
					"appid": API_key,      
					"units": "metric"       # Units of measurement ('metric' for °C, 'imperial' for °F)
				}

				url = "https://api.openweathermap.org/data/2.5/weather"

				response = requests.get(url, params=params)

				if response.status_code == 200:
					data = response.json()
					main = data.get("main", {})
					wind = data.get("wind", {})
					clouds = data.get("clouds", {})
					rain = data.get("rain", {})
					
					temp = main.get("temp")
					rh = main.get("humidity")
					ws = wind.get("speed")
					r = rain.get("1h", 0)
					final_result = {
						"temperature" : f"{temp} °C",
						"humidity" : f"{rh} %",
						"wind_speed" : f"{ws} km/h",
						"rain" : f"{r} mm",
						# "cloud_cover" : clouds.get("all"),
					}
					return Response(final_result, status=status.HTTP_200_OK)
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error	
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response("Error in APi", status=status.HTTP_404_NOT_FOUND)


class weather(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		
		field_id 	= request.query_params.get('field_id')
		end_date 	= (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
		start_date	= (datetime.now() - timedelta(weeks=8)).strftime('%Y-%m-%d')

		if field_id != None and start_date != None and end_date != None:

			try :
				user = request.user
				field = Field.objects.get(id=field_id, user_id=user.id) # 
				point = field.boundaries[0][0]
				lat = point[1]
				lon = point[0]
				# print(field_id, lat, lon)
				final_result = {
					'historic' : historic_weather(lat, lon, start_date, end_date),
					'forcast'	: forcast(lat, lon)
				}
				# print(final_result['historic'])
				return Response(final_result, status=status.HTTP_200_OK)
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error	
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response("Error in APi", status=status.HTTP_404_NOT_FOUND)
	
class Forcast(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		
		field_id = request.query_params.get('field_id')
		
		if field_id != None:

			try :
				user = request.user
				field = Field.objects.get(id=field_id, user_id=user.id) # 
				point = field.boundaries[0][0]
				lat = point[1]
				lon = point[0]
				final_result = forcast(lat, lon)
				return Response(final_result, status=status.HTTP_200_OK)
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error	
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response("Error in APi", status=status.HTTP_404_NOT_FOUND)


class gdd(APIView):
	
	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):

		start_date = request.query_params.get('start_date')
		end_date = request.query_params.get('end_date')
		field_id = request.query_params.get('field_id')

		if field_id != None and start_date != None and end_date != None:

			try :

				user = request.user
				field = Field.objects.get(id=field_id, user_id=user.id) # 
				point = field.boundaries[0][0]
				lat = point[1]
				lon = point[0]
				final_data = gdd_weather(lat, lon, start_date, end_date)
				
				return Response(final_data, status=status.HTTP_200_OK)
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error	
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response("Error in data", status=status.HTTP_404_NOT_FOUND)
