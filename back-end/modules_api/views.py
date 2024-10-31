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
import os
import rasterio
import numpy as np
import requests

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

class fao_test(APIView):


	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def extract_date(file_name):
		return datetime.strptime(file_name.split('.')[0], '%Y-%m-%d')

	def post(self, request):

		start_date	= request.data.get('start_date')
		end_date	= request.data.get('end_date')
		path		= "/app/tools/fao_test/fao_output"
		folders		= os.listdir(path)

		final_data = []
		try : 
			for folder in folders:
				min_values, max_values, mean_values = [], [], []
				var = f"{path}/{folder}"
				files = [f for f in os.listdir(var) if os.path.isfile(os.path.join(var, f))]

				files = sorted(files, key=self.extract_date)
				x, y = files.index(f"{start_date}.tif"), files.index(f"{end_date}.tif")
				files = files[x:y]
				for file in files:
					tif = f"{var}/{file}"
					with rasterio.open(tif) as src:
						
						data = src.read(1)
						mean, min, max = np.nanmean(data), np.nanmin(data), np.nanmax(data)
						min_values.append(min), mean_values.append(mean), max_values.append(max)
						break 
				
				final_data[folder] = {
						'min' :  min_values,
						'max'  : max_values,
						'mean' : mean_values
					}

		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		return Response(final_data, status=status.HTTP_202_ACCEPTED)

class current_weather(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):

		field_id = request.query_params.get('field_id')

		if field_id != None:

			try : 
				API_key = "85461dddb7698ac03b2bf4c5b22f5369"
				field = Field.objects.get(id=field_id)
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

					final_result = {
						"temperature" : main.get("temp"),
						"humidity" : main.get("humidity"),
						"wind_speed" : wind.get("speed"),
						# "cloud_cover" : clouds.get("all"),
						"rain" : rain.get("1h", 0),
					}
					return Response(final_result, status=status.HTTP_200_OK)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response("Error in APi", status=status.HTTP_404_NOT_FOUND)


class weather(APIView):

	# authentication_classes = [FARMERJWTAuthentication]
	# permission_classes = [IsAuthenticated]

	def get(self, request):
		
		field_id = request.query_params.get('field_id')
		start_date = request.query_params.get('start_date')
		end_date = request.query_params.get('end_date')
		
		print(field_id)
		if field_id != None:

			try :
	
				field = Field.objects.get(id=field_id)
				point = field.boundaries[0][0]
				lat = point[1]
				lon = point[0]
				url = "https://archive-api.open-meteo.com/v1/archive"

				# Define parameters for the API request
				params = {
					"latitude": lat,  
					"longitude": lon,  
					"start_date": start_date,  
					"end_date": end_date,  # End date for historical data
					# "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,shortwave_radiation",  # Request hourly data for temperature, precipitation, wind speed, RH, and shortwave radiation
					"daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max",
					"timezone": "Africa/Casablanca", 
					"windspeed_unit": "ms",        # kmh, ms, mph, kn
				}


				# Send the request to the Open-Meteo API
				response = requests.get(url, params=params)

				# Check if the request was successful
				if response.status_code == 200:
					data = response.json()

					final_result = {
						"dates"	: data.get('daily')["time"],
						"T2m"	:  data.get('daily')["temperature_2m_max"],
						"rain" 	: data.get('daily')["rain_sum"],
						"irg" 	: data.get('daily')["shortwave_radiation_sum"],
						"Et0" 	: data.get("daily")["et0_fao_evapotranspiration"],
						"Rh" 	:  data.get("daily")["relative_humidity_2m_max"],
						"Ws" 	: data.get("daily")["wind_speed_10m_max"]
					}

					return Response(final_result, status=status.HTTP_200_OK)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response("Error in APi", status=status.HTTP_404_NOT_FOUND)