from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from models_only.models import Field, Soil 
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt 
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from .tools.functions_tools import get_user_by_email
from .tools.FarmerAUTH import FARMERJWTAuthentication
from django.contrib.gis.geos import GEOSGeometry
import json
from django.db import transaction


class register(APIView):

	permission_classes = [AllowAny]

	@swagger_auto_schema(
		request_body=FarmerSerializer,
		responses={201: FarmerSerializer}
	)

	def post(self, request):

		if email_exists(request.data.get("email")):
			return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
		
		if request.data.get('type') != None:
			user_type = request.data.get('type')
		
		serializer = FarmerSerializer(data=request.data)
		if serializer.is_valid() :

			try :
				user = serializer.save()
				refresh = RefreshToken.for_user(user)
				refresh['user_type'] = user_type
				refresh_token = str(refresh)
				return Response({'access_token': str(refresh.access_token),
								'refresh_token': refresh_token,
								'type' : user_type,
							},
							status=status.HTTP_201_CREATED)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
				

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class login(APIView):

	permission_classes = [AllowAny]

	@swagger_auto_schema(
		request_body=loginSerializer,
		responses={201: loginSerializer}
	)

	def post(self, request):
		serializer = loginSerializer(data=request.data)

		if serializer.is_valid():
			email = serializer.validated_data.get('email')
			password = serializer.validated_data.get('password')
			
			try :

				user, user_type = get_user_by_email(email)
				if user is None:
					return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

				if not user.check_user_password(password):
					return Response({"message": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)

				refresh = RefreshToken.for_user(user)
				refresh['user_type'] = user_type

				return Response({
					'access_token': str(refresh.access_token),
					'refresh_token': str(refresh),
					'type' : user_type
				}, status=status.HTTP_201_CREATED)
	
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class field(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		
		user = request.user
		try : 

			fields = Field.objects.filter(user_id=user.id)
			if fields.exists():
				fields_data = [{'id' : field.id, 'name': field.name, 'boundaries': json.loads(field.boundaries.geojson)} for field in fields]
				return Response(fields_data, status=status.HTTP_200_OK)

		except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({"detail": "No fields found for this user."}, status=status.HTTP_404_NOT_FOUND)
	
	@swagger_auto_schema(
        request_body=FieldSerializer,
        responses={201: FieldSerializer}
    )

	def post(self, request):
		serializer = FieldSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			try :
				serializer.save()
				return Response({"message": "Field created successfully"}, status=status.HTTP_201_CREATED)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	@swagger_auto_schema(
	    request_body=openapi.Schema(
	        type=openapi.TYPE_OBJECT,
	        properties={
	            'field_id': openapi.Schema(type=openapi.TYPE_INTEGER),
			},
	    ),
	)
	def delete(self, request):
		
		field_id = request.data.get('field_id')

		if field_id != None:
			try :
				Field.objects.filter(id=field_id).delete()
				return Response({"message": "Field deleted successfully"}, status=status.HTTP_201_CREATED)
			except Exception as e:
					return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
	
class soil(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	# def get(self, request):

	# 	user_id = request.user
	# 	soil = Soil.objects.filter(user_id=user_id.id)
	# 	if soil.exists():
	# 		fields_data = [{'name': i.soil_type} for i in soil]
	# 		return Response(fields_data, status=status.HTTP_200_OK)
	# 	else:
	# 		return Response({"detail": "No soil found for this user."}, status=status.HTTP_404_NOT_FOUND)

	def post(self, request):
		pass

# class season(APIView):

	# authentication_classes = [FARMERJWTAuthentication]
	# permission_classes = [IsAuthenticated]
	
	# @swagger_auto_schema(
	# 	manual_parameters=[
    #         openapi.Parameter('field_id', openapi.IN_QUERY, description="ID of the field", type=openapi.TYPE_INTEGER)
	# 	],
	# 	responses={200: SeasonSerializer(many=True)}
	# )

	# def get(self, request):
	# 	field_id = request.query_params.get('field_id')
		
	# 	if not field_id:
	# 		return Response({"error": "Field ID is required"}, status=status.HTTP_400_BAD_REQUEST)
	# 	try :

	# 		seasons = Season.objects.filter(field_id=field_id)
	# 		if seasons.exists():
	# 				seasons_data = [{'id' : _season.id, 'start_date' : _season.start_date} for _season in seasons]
	# 				return Response(seasons_data, status=status.HTTP_200_OK)
	
	# 	except Exception as e:
	# 		return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
	# 	return Response({"detail": "No Season found for this field."}, status=status.HTTP_404_NOT_FOUND)

	@swagger_auto_schema(
		request_body=SeasonSerializer,
		responses={201: SeasonSerializer}
	)
	def post(self, request):
		serializer = SeasonSerializer(data=request.data)
		if serializer.is_valid():
			try:
				serializer.save()
				return Response({"message": "Season created successfully"}, status=status.HTTP_201_CREATED)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Delete season",
		request_body=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'season_id': openapi.Schema(type=openapi.TYPE_INTEGER),
			},
		),
		responses={202: 'Season has been deleted successfully', 400: 'Bad request'}
	)
	def delete(self, request):
		season_id = request.data.get('season_id')
		if season_id:
			try:
				p = Season.objects.filter(id=season_id).delete()
				if p[0] == 1:
					return Response({'message': 'Season has been deleted successfully'}, status=status.HTTP_202_ACCEPTED)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class register_data(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def process_season(self, season, field):
		new_season = Season(start_date = season.get('date'),
							field_id=field)
		new_season.save()
		return new_season

	def process_soil(self, soil_type, field):
		
		_type = {
			'LOAMY SAND' : 'LOAMY_SAND',
			'SANDY CLAY LOAM' : 'SANDY_CLAY_LOAM',
			'CLAY LOAM' : 'CLAY_LOAM',
			'SILTY CLAY' : 'SILTY_CLAY',
			'SANDY CLAY' : 'SANDY_CLAY',
			'SANDY LOAM' : 'SANDY_LOAM'

		}.get(soil_type, soil_type)

		new_soil = Soil(soil_type=Soil_type[_type].name,
				  		field_id=field)
		new_soil.save()
	
	def process_irrigation_system(self, irrigation_data, field):
		
		irg_type = irrigation_data['system']
		prop = irrigation_data['prop']

		irg_class = {
			'Rainfed irrigation': Irrigation_system,
			'Surface irrigation': Surface_irrigation,
			'Drip irrigation': Drip_Irrigation,
			'Sprinkler irrigation' : Sprinkler_irrigation
		}.get(irg_type)
		
		# installation_date = irrigation_data.get('installation_date', None)
	
		_type = {
			'Sprinkler irrigation' : 'Sprinkler',
			'Surface irrigation' : 'Surface',
			'Drip irrigation' : 'Drip',
			'Rainfed irrigation' : 'Rainfed'
		}.get(irg_type)
	
		irrigation_kwargs = {
        	'irrigation_type': Irrigation_type[_type].name,
        	'field_id': field,
    	}

		if irg_type == 'Drip irrigation':
			irrigation_kwargs.update({
				'Tubes_distance': prop.get('DistanceBetweenTubes', None),
				'Drippers_distance': prop.get('DistanceBetweenDrippers', None),
				'drippers_area': prop.get('CoverageAreaOfEachDrippers', None)
			})

		elif irg_type == 'Sprinkler irrigation':
			irrigation_kwargs.update({
				'radius' : prop.get('SprinklerRadius', None),
				'coverage_area' : prop.get('sprinklerCoverage', None),
				'outflow_rate' : prop.get('WaterOutflowRate', None),
				'number_in_use' : prop.get('numberOfSprinklers', None)
			})

		irg_class.objects.create(**irrigation_kwargs)

	def process_crop(self, crop_data, season):
		Crop.objects.create(Season=season, type=crop_data.get('type'), value=crop_data.get('value'))


	def post(self, request):

		if all([request.data.get('field'), request.data.get('irr'), request.data.get('soil'),
		  	request.data.get('planting')]):
			with transaction.atomic():

				fieldSerializer = FieldSerializer(data=request.data.get('field'), context={'request': request})
				if fieldSerializer.is_valid():
					try :

						field = fieldSerializer.save()
						self.process_soil(request.data.get('soil'), field)
						self.process_irrigation_system(request.data.get('irr'), field)
						new_season = self.process_season(request.data.get('planting'), field)
						self.process_crop(request.data.get('planting'), new_season)
	
					except Exception as e:
						return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
			return Response("Data stored successfully", status=status.HTTP_201_CREATED)
		return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
		
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
