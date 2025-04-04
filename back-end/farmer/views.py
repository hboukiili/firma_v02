# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from firma_v02.auth import IsFarmer
from models_only.models import Field, Soil, Crop
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
import jwt 
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.gis.geos import GEOSGeometry
import json
from django.db import transaction
from django.utils.html import escape
import logging
from celery.result import AsyncResult
# from ratelimit.decorators import ratelimit
from modules_api.tasks import process_new_field
import os
import rasterio
from shapely.wkt import loads
import geopandas as gpd
from django.forms.models import model_to_dict
import numpy as np
logger = logging.getLogger(__name__)

from .serializer import UserRegistrationSerializer

class register(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)

	
class login(TokenObtainPairView):

    """
    Returns the JWT tokens and also sets them in HttpOnly cookies.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access_token = data.get('access')
            refresh_token = data.get('refresh')
            # Set the cookies. Adjust parameters as needed.
            access_cookie_max_age = int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
            refresh_cookie_max_age = int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
            
            response.set_cookie(
                'access_token',
                access_token,
                max_age=access_cookie_max_age,
                httponly=True,
                secure=False,  # Use True in production
                samesite='Lax'
            )
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=refresh_cookie_max_age,
                httponly=True,
                secure=False,
                samesite='Lax'
            )
        return response


class field(APIView):

    permission_classes = [IsFarmer]

    def get(self, request):
		
        user = request.user
        print(user.id, 'heeereeee')
        try : 

			# fields = Field.objects.all()

			# for field in fields:
			# 		process_new_field.delay(field.id, field.boundaries.wkt, field.boundaries[0][0])

            fields = Field.objects.filter(user_id=user.id)
            if fields.exists():
                fields_data = [{'id' : field.id, 'name': field.name, 'boundaries': json.loads(field.boundaries.geojson)} for field in fields]
                # wkt = []
                # for field in fields:
                # 	wkt.append(loads(field.boundaries.wkt))
                # gdf = gpd.GeoDataFrame(geometry=wkt, crs="EPSG:4326")
                # gdf.to_file('/app/shapefile.shp', driver="ESRI Shapefile")
                return Response(fields_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "No fields found for this user."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        serializer = FieldSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try :
                serializer.save()
                return Response({"message": "Field created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	# def delete(self, request):
		
	# 	field_id = request.data.get('field_id')

	# 	if field_id != None:
	# 		try :
	# 			Field.objects.filter(id=field_id).delete()
	# 			return Response({"message": "Field deleted successfully"}, status=status.HTTP_201_CREATED)
	# 		except Exception as e:
	# 				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
	
# # class soil(APIView):

# # 	authentication_classes = [FARMERJWTAuthentication]
# # 	permission_classes = [IsAuthenticated]

# 	# def get(self, request):

# 	# 	user_id = request.user
# 	# 	soil = Soil.objects.filter(user_id=user_id.id)
# 	# 	if soil.exists():
# 	# 		fields_data = [{'name': i.soil_type} for i in soil]
# 	# 		return Response(fields_data, status=status.HTTP_200_OK)
# 	# 	else:
# 	# 		return Response({"detail": "No soil found for this user."}, status=status.HTTP_404_NOT_FOUND)

# 	# def post(self, request):
# 	# 	pass

# # class season(APIView):

# # 	authentication_classes = [FARMERJWTAuthentication]
# # 	permission_classes = [IsAuthenticated]
	
# 	# @swagger_auto_schema(
# 	# 	manual_parameters=[
#     #         openapi.Parameter('field_id', openapi.IN_QUERY, description="ID of the field", type=openapi.TYPE_INTEGER)
# 	# 	],
# 	# 	responses={200: SeasonSerializer(many=True)}
# 	# )

# 	# def get(self, request):
# 	# 	field_id = request.query_params.get('field_id')
		
# 	# 	if not field_id:
# 	# 		return Response({"error": "Field ID is required"}, status=status.HTTP_400_BAD_REQUEST)
# 	# 	try :

# 	# 		seasons = Season.objects.filter(field_id=field_id)
# 	# 		if seasons.exists():
# 	# 				seasons_data = [{'id' : _season.id, 'start_date' : _season.start_date} for _season in seasons]
# 	# 				return Response(seasons_data, status=status.HTTP_200_OK)
	
# 	# 	except Exception as e:
# 	# 		return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# 	# 	return Response({"detail": "No Season found for this field."}, status=status.HTTP_404_NOT_FOUND)

# 	# @swagger_auto_schema(
# 	# 	request_body=SeasonSerializer,
# 	# 	responses={201: SeasonSerializer}
# 	# )
# 	# def post(self, request):
# 	# 	serializer = SeasonSerializer(data=request.data)
# 	# 	if serializer.is_valid():
# 	# 		try:
# 	# 			serializer.save()
# 	# 			return Response({"message": "Season created successfully"}, status=status.HTTP_201_CREATED)
# 	# 		except Exception as e:
# 	# 			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# 	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 	# @swagger_auto_schema(
# 	# 	operation_description="Delete season",
# 	# 	request_body=openapi.Schema(
# 	# 		type=openapi.TYPE_OBJECT,
# 	# 		properties={
# 	# 			'season_id': openapi.Schema(type=openapi.TYPE_INTEGER),
# 	# 		},
# 	# 	),
# 	# 	responses={202: 'Season has been deleted successfully', 400: 'Bad request'}
# 	# )
# 	# def delete(self, request):
# 	# 	season_id = request.data.get('season_id')
# 	# 	if season_id:
# 	# 		try:
# 	# 			p = Season.objects.filter(id=season_id).delete()
# 	# 			if p[0] == 1:
# 	# 				return Response({'message': 'Season has been deleted successfully'}, status=status.HTTP_202_ACCEPTED)
# 	# 		except Exception as e:
# 	# 			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# 	# 	return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

SOIL_METHODS = {
    'Selection': 'Selection',
    'Composition': 'Composition'
}

IRRIGATION_TYPES = {
    'Rainfed irrigation': 'Rainfed',
    'Surface irrigation': 'Surface',
    'Drip irrigation': 'Drip',
    'Sprinkler irrigation': 'Sprinkler'
}

class RegisterData(APIView):

    permission_classes = [IsFarmer]

    def process_soil(self, method, value, field):
        soil_kwargs = {
            'field_id': field,
            'soil_input_method': soil_input[method.lower()].name
        }

        if method == SOIL_METHODS['Selection']:
            soil_type_mapping = {
                'LOAMY SAND': 'LOAMY_SAND',
                'SANDY CLAY LOAM': 'SANDY_CLAY_LOAM',
                'CLAY LOAM': 'CLAY_LOAM',
                'SILTY CLAY': 'SILTY_CLAY',
                'SANDY CLAY': 'SANDY_CLAY',
                'SANDY LOAM': 'SANDY_LOAM'
            }
            _type = soil_type_mapping.get(value, value)
            soil_kwargs['soil_type'] = Soil_type[_type].name

        elif method == SOIL_METHODS['Composition']:
            soil_kwargs.update({
                'sand_percentage': value['sand'],
                'silt_percentage': value['silt'],
                'clay_percentage': value['clay']
            })

        Soil.objects.create(**soil_kwargs)

    def process_irrigation_system(self, irrigation_data, field):
        irg_type = irrigation_data['system']
        prop = irrigation_data['prop']

        irg_class = {
            'Rainfed irrigation': Irrigation_system,
            'Surface irrigation': Surface_irrigation,
            'Drip irrigation': Drip_Irrigation,
            'Sprinkler irrigation': Sprinkler_irrigation
        }.get(irg_type)

        irrigation_kwargs = {
            'irrigation_type': Irrigation_type[IRRIGATION_TYPES[irg_type]].name,
            'field_id': field,
        }

        if irg_type == 'Drip irrigation':
            irrigation_kwargs.update({
                'Crop_Tubes_distance': prop.get('DistanceBetweenTubes_c', None),
                'Crop_Drippers_distance': prop.get('DistanceBetweenDrippers_c', None),
                'Tree_row_distance': prop.get('DistanceBetweenRows_t', None),
                'Tree_distance': prop.get('DistanceBetweenTrees_t', None),
                'Tubes_number_by_tree': prop.get('NumberOfTubesPerTree_t', None),
                'drippers_number_by_tree': prop.get('NumberOfDrippersPerTree_t', None),
                'Tree_outflow_rate': prop.get('WaterOutflowRate_t', None)
            })

        elif irg_type == 'Sprinkler irrigation':
            irrigation_kwargs.update({
                'coverage_area': prop.get('sprinklerCoverage_c', None),
                'outflow_rate': prop.get('WaterOutflowRate_c', None),
                'number_of_sprinklers': prop.get('numberOfSprinklers_c', None)
            })

        irg_class.objects.create(**irrigation_kwargs)

    def process_crop(self, data, field):
        crop = data['Crop']
        tree = data['Tree']

        Crop.objects.create(
            Crop=crop['value'],
            Crop_planting_date=crop['date'],
            Tree=tree['value'],
            Tree_planting_date=tree['date'],
            field_id=field
        )

    def post(self, request):
        required_fields = ['field', 'irr', 'soil', 'plant']
        if not all(request.data.get(field) for field in required_fields):
            return Response("Missing required fields", status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            field_serializer = FieldSerializer(data=request.data.get('field'), context={'request': request})
            if field_serializer.is_valid():
                try:
                    field = field_serializer.save()
                    self.process_soil(request.data['soil']['method'], request.data['soil']['value'], field)
                    self.process_irrigation_system(request.data['irr'], field)
                    self.process_crop(request.data['plant'], field)

                    logger.info('Starting the process...')
                    # task_id = process_new_field.delay(field.id, field.boundaries.wkt, field.boundaries[0][0])
                    # logger.info(f"Task ID: {task_id.id}")
                    return Response('task_id.id', status=status.HTTP_201_CREATED)

                except Exception as e:
                    logger.error(f"Error occurred during data processing: {str(e)}")
                    return Response({"error": "An error occurred while processing your request"},
						status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(field_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		# season = Season()
		# field = Field.objects.get(id=1)
		# new_irrigation_system = Surface_irrigation.objects.create(
		# 	irrigation_type=Irrigation_type.Surface.name,  
		# 	field_id=field 
		# )
		# new_irrigation_system.save()
		# test = Irrigation_system.objects.select_related().filter(field_id=field)
		# for i in test:
		# print(i.irrigation_type)

class Irrigation(APIView):

    permission_classes = [IsFarmer]

    def get_fc_value(self, field_id):

        path = f'Data/fao_output/{field_id}/fc'

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        files = sorted(files, key=lambda x: x.split('.')[0])
        with rasterio.open(f"{path}/{files[-1]}") as tif:
          fc = tif.read(1)
          fc_mean = np.nanmean(fc)
          return fc_mean

    def calculate_irrigation_duration_dripp(self, mm, disTubes, disDr, outflowRate):

        """
        Calculate the irrigation duration based on the desired water depth and application parameters.

        Parameters:
          mm (float): Desired water depth in millimeters.
          disTubes (float): Length or one dimension of the area (in meters).
          disDr (float): The other dimension of the area (in meters).
          outflowRate (float): Application rate (in cubic meters per minute).

        Returns:
          float: The duration required (in minutes).
        """
		# Convert mm to m, compute the volume, then divide by the outflow rate.
        duration = mm * disTubes * disDr / outflowRate
        fractional_part = duration - int(duration)
        fractional_part = int(fractional_part * 60)
        if fractional_part == 0 and int(duration) == 0: return ('0H2M')
        return f'{str(int(duration))}h {str(fractional_part)}m'


    def post(self, request):

        field_id				= request.data.get('field_id')
        irrigation_Amount 		= request.data.get('value')
        date					= request.data.get('date')
        Unity					= request.data.get('unity')

		# print(field_id, date, Unity, irrigation_Amount)
        if field_id and irrigation_Amount and date and Unity:
            try :
                user = request.user
                irrigation = Irrigation_system.objects. \
                    select_related('field_id').get(field_id=field_id) #field_id__user_id=user.id
                if Unity == 'hour':
                
                    fc = self.get_fc_value(field_id)

                    if irrigation.irrigation_type == 'Drip':
                        drip = Drip_Irrigation.objects.get(field_id=field_id)
                        c4 = int(irrigation_Amount)
                        if drip.Crop_Tubes_distance != None:
                            c1 = drip.Crop_Tubes_distance
                            c2 = drip.Crop_Drippers_distance
                            c3 = drip.Crop_outflow_rate
                            irrigation_Amount = (c4 * c3) / (c1 * c2 * fc)
                        elif drip.Tree_outflow_rate != None:
                            T1 = drip.Tree_row_distance
                            T2 = drip.Tree_distance
                            T3 = drip.drippers_number_by_tree
                            T4 = drip.Tree_outflow_rate
                            irrigation_Amount = (T4 * T3 * c4) / (T1 * T2 * fc)

                if irrigation != None:
                    new_irr = Irrigation_amount(amount=irrigation_Amount, date=date,irrigation_system_id=irrigation, amount_type=Unity)
                    new_irr.save()

                    return Response(status=status.HTTP_201_CREATED)
			
            except Exception as e:
                logger.error(f"Error occurred during data processing: {str(e)}")  # Log error
                return Response({f"error": "An error occurred while processing your request : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response("Error in Data", status=status.HTTP_400_BAD_REQUEST)

    def all_thefields(self, user):


        irrigation_qs = Irrigation_amount.objects.filter(
			irrigation_system_id__field_id__user_id=user.id,
			amount__gt=0
		).select_related('irrigation_system_id', 'irrigation_system_id__field_id').order_by('id')

        data = []
        for ia in irrigation_qs:
            drip = Drip_Irrigation.objects.get(field_id=ia.irrigation_system_id.field_id.id)
            duration = self.calculate_irrigation_duration_dripp(ia.amount, drip.Crop_Tubes_distance, drip.Crop_Drippers_distance, drip.Crop_outflow_rate)
            data.append({
                'ammount_id' : ia.id,
                'date': ia.date.strftime('%Y-%m-%d'),
                'amount': duration,
                'amount_type': ia.amount_type,
                'name': ia.irrigation_system_id.field_id.name,
            })

        return data

    def irrigation_by_field(self, field_id):

        irrigation_qs = Irrigation_amount.objects.filter(
				irrigation_system_id__field_id=field_id,
				amount__gt=0
		).order_by('date')

        dates = []
        amount = []
        for ia in irrigation_qs:
            drip = Drip_Irrigation.objects.get(field_id=ia.irrigation_system_id.field_id.id)
            duration = self.calculate_irrigation_duration_dripp(ia.amount, drip.Crop_Tubes_distance, drip.Crop_Drippers_distance, drip.Crop_outflow_rate)
            dates.append(ia.date.strftime('%Y-%m-%d'))
            amount.append(duration)

        return {
			'dates' : dates,
			'duration' : amount,
		}


    def get(self, request):

        user = request.user
        try :
          if 'field_id' in request.query_params:
              data = self.irrigation_by_field(request.query_params.get('field_id'))
          else:
              data = self.all_thefields(user)
          return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
          logger.error(f"Error occurred during data processing: {str(e)}")  # Log error
          return Response({f"error": "An error occurred while processing your request : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class recommandation(APIView):


	def get(self, request):

		if 'field_id' in request.query_params:
			try :

				recommandation = None
				field_id = request.query_params.get('field_id')
				drip = Drip_Irrigation.objects.get(field_id=field_id)
				path = f'/app/Data/fao_output/{field_id}/Irrig'
				files = sorted([f for f in os.listdir(path) if f.endswith(".tif")], key=lambda x: x.split('.')[0])
				with rasterio.open(os.path.join(path, files[-6])) as src:
					irr = src.read(1)
					if np.nanmean(irr):
						recommandation = { 
							'duration' : Irrigation.calculate_irrigation_duration_dripp('',np.nanmean(irr), drip.Crop_Tubes_distance, drip.Crop_Drippers_distance, drip.Crop_outflow_rate),
							'date' : files[0].split('_')[1].split('_')[0]
						}
				latest_irrigation = Irrigation_amount.objects.filter(
						irrigation_system_id__field_id=field_id,
						amount__gt=0
					).order_by('-date').first()
				data = model_to_dict(latest_irrigation)
				latest = {
					'duration' : Irrigation.calculate_irrigation_duration_dripp('',data['amount'], drip.Crop_Tubes_distance, drip.Crop_Drippers_distance, drip.Crop_outflow_rate),
					'date' : data['date']
				}
				return Response({'latest' : latest, 'recommandation' : recommandation}, status=status.HTTP_200_OK)
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error
				return Response({f"error": "An error occurred while processing your request : {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

		return Response("Error in Data", status=status.HTTP_400_BAD_REQUEST)

class check_pro(APIView):
	
	def get(self, request):


		task_id = request.query_params.get('task_id')
		result = AsyncResult(task_id)

		if result.ready():
			if result.successful():
				return Response("Done", status=status.HTTP_200_OK)
			else:
				return Response(f"Error : {result.result}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else :
			return Response("Task is still running")

# import requests
# import csv
# import pandas as pd
# def send_req(field_id, date, value, unity='m³'):
	
# 	payload = {
# 		'field_id' : field_id,
# 		'date' : date,
# 		'value' : value,
# 		'unity' : unity
# 	}

# 	response = requests.post('http://localhost:8000/farmer/irr', json=payload)
# 	print(response.status_code)

# class test(APIView):

# 	def get(self, request):
		
# 		fields = {
# 			'E3P2' : '32',
# 			'E3P1' : '34',
# 			'E3P4' : '35',
# 			'E3P3' : '36',
# 			'E3P6' : '37',
# 			'E3P8' : '38',
# 			'E3P7' : '39',
# 			'E3P5' : '40',
# 			'E2P6' : '41',
# 			'E2P5' : '42',
# 			'E2P7' : '43',
# 			'E2P4' : '44',
# 			'E2P3' : '45',
# 			'E2P2' : '46',
# 			'E2P1' : '47',
# 		}
# 		df = pd.read_csv('/app/tools/irrigation parcelle lraba 18_02_2025(Feuil1).csv', sep=';')
# 		df.drop('date',axis=1, inplace=True)
# 		start_date = "2024-12-17"
# 		end_date = '16-02-2025'

# 		# # Generate a date range and format it as strings
# 		date_range = pd.date_range(start=start_date, end=end_date)
# 		dates_str = date_range.strftime("%Y-%m-%d").tolist()
# 		for i in df:
# 			field_id = fields[i]
# 			x = 0
# 			while (x < len(date_range)):
# 				send_req(field_id, dates_str[x], df[i][x])
# 				# print(field_id, dates_str[x], df[i][x])
# 				x += 1

# 		# fields = Field.objects.all()	
# 		# for field in fields:
# 		# 	print(field.id, field.name)
# 		# 	if field.id == 32 or field.id == 34 or field.id == 35:
# 		# 		continue
# 		# 	path = f"/app/Data/fao_output/{field.id}/Irrig"
# 		# 	files = sorted([f for f in os.listdir(path) if f.endswith(".tif")], key=lambda x: x.split('.')[0])
# 		# 	send_req(field.id, '2024-12-16', 0)
# 		# 	for file in files:
# 		# 		date = file.split('_')[1].split('.')[0]
# 		# 		with rasterio.open(os.path.join(path, file)) as src:
# 		# 			ndvi = src.read(1)
# 		# 			send_req(field.id, date, float(np.nanmean(ndvi)))
# 		return Response("No ...")