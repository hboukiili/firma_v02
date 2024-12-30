from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from models_only.models import Field, Soil, Crop
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
from django.utils.html import escape
import logging
from celery.result import AsyncResult
# from ratelimit.decorators import ratelimit
from modules_api.tasks import process_new_field

logger = logging.getLogger(__name__)



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
	
# class soil(APIView):

# 	authentication_classes = [FARMERJWTAuthentication]
# 	permission_classes = [IsAuthenticated]

	# def get(self, request):

	# 	user_id = request.user
	# 	soil = Soil.objects.filter(user_id=user_id.id)
	# 	if soil.exists():
	# 		fields_data = [{'name': i.soil_type} for i in soil]
	# 		return Response(fields_data, status=status.HTTP_200_OK)
	# 	else:
	# 		return Response({"detail": "No soil found for this user."}, status=status.HTTP_404_NOT_FOUND)

	# def post(self, request):
	# 	pass

# class season(APIView):

# 	authentication_classes = [FARMERJWTAuthentication]
# 	permission_classes = [IsAuthenticated]
	
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

	# @swagger_auto_schema(
	# 	request_body=SeasonSerializer,
	# 	responses={201: SeasonSerializer}
	# )
	# def post(self, request):
	# 	serializer = SeasonSerializer(data=request.data)
	# 	if serializer.is_valid():
	# 		try:
	# 			serializer.save()
	# 			return Response({"message": "Season created successfully"}, status=status.HTTP_201_CREATED)
	# 		except Exception as e:
	# 			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# @swagger_auto_schema(
	# 	operation_description="Delete season",
	# 	request_body=openapi.Schema(
	# 		type=openapi.TYPE_OBJECT,
	# 		properties={
	# 			'season_id': openapi.Schema(type=openapi.TYPE_INTEGER),
	# 		},
	# 	),
	# 	responses={202: 'Season has been deleted successfully', 400: 'Bad request'}
	# )
	# def delete(self, request):
	# 	season_id = request.data.get('season_id')
	# 	if season_id:
	# 		try:
	# 			p = Season.objects.filter(id=season_id).delete()
	# 			if p[0] == 1:
	# 				return Response({'message': 'Season has been deleted successfully'}, status=status.HTTP_202_ACCEPTED)
	# 		except Exception as e:
	# 			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
	# 	return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class register_data(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]


	def process_soil(self, method, value, field):
			
		if method == 'Selection':
	
			_type = {
				'LOAMY SAND' : 'LOAMY_SAND',
				'SANDY CLAY LOAM' : 'SANDY_CLAY_LOAM',
				'CLAY LOAM' : 'CLAY_LOAM',
				'SILTY CLAY' : 'SILTY_CLAY',
				'SANDY CLAY' : 'SANDY_CLAY',
				'SANDY LOAM' : 'SANDY_LOAM'
			}.get(value, value)

			new_soil = Soil(soil_type=Soil_type[_type].name,
							field_id=field, soil_input_method=soil_input[method.lower()].name)
			new_soil.save()
		
		elif method == 'Composition':
			
			new_soil = Soil(sand_percentage=value['sand'], 
				   silt_percentage=value['silt'],
				   clay_percentage=value['clay'], field_id=field,
				   soil_input_method=soil_input[method.lower()].name)
			new_soil.save()
	
	def process_irrigation_system(self, irrigation_data, field):

		irg_type	= irrigation_data['system']
		prop 		= irrigation_data['prop']

		irg_class = {
			'Rainfed irrigation'	: Irrigation_system,
			'Surface irrigation'	: Surface_irrigation,
			'Drip irrigation'		: Drip_Irrigation,
			'Sprinkler irrigation'	: Sprinkler_irrigation
		}.get(irg_type)

		_type = {
			'Sprinkler irrigation'	: 'Sprinkler',
			'Surface irrigation' 	: 'Surface',
			'Drip irrigation' 		: 'Drip',
			'Rainfed irrigation' 	: 'Rainfed'
		}.get(irg_type)


		irrigation_kwargs = {
        	'irrigation_type'		: Irrigation_type[_type].name,
        	'field_id'				: field,
    	}

		if irg_type == 'Drip irrigation':
			irrigation_kwargs.update({
				'Crop_Tubes_distance'	 : prop.get('DistanceBetweenTubes_c', None),
				'Crop_Drippers_distance' : prop.get('DistanceBetweenDrippers_c', None),
				'Tree_row_distance'		 : prop.get('DistanceBetweenRows_t', None),
				'Tree_distance'			 : prop.get('DistanceBetweenTrees_t', None),
				'Tubes_number_by_tree'	 : prop.get('NumberOfTubesPerTree_t', None),
				'drippers_number_by_tree': prop.get('NumberOfDrippersPerTree_t', None),
				'Tree_outflow_rate'		 : prop.get('WaterOutflowRate_t', None)
			})

		elif irg_type == 'Sprinkler irrigation':
			irrigation_kwargs.update({
				'coverage_area' 		: prop.get('sprinklerCoverage_c', None),
				'outflow_rate' 			: prop.get('WaterOutflowRate_c', None),
				'number_of_sprinklers'	: prop.get('numberOfSprinklers_c', None)
			})

		irg_class.objects.create(**irrigation_kwargs)
		# process_new_field.delay(field.id, field.boundaries.wkt, field.boundaries[0][0])

	def process_crop(self, data, field):
		crop		= data['Crop']
		tree 		= data['Tree']
		crop_name	= crop['value']
		tree_name	= tree['value']

		new_crop = Crop(Crop=crop_name, Crop_planting_date=crop['date'],
	   			Tree=tree_name, Tree_planting_date=tree['date'],
				field_id=field)

		new_crop.save()

	# @ratelimit(key='user', rate='5/m', method='POST', block=True)
	def post(self, request):


		if all([request.data.get('field'), request.data.get('irr'), request.data.get('soil'),
		  	request.data.get('plant')]):
			with transaction.atomic():

				fieldSerializer = FieldSerializer(data=request.data.get('field'), context={'request': request})
				if fieldSerializer.is_valid():
					try :
						field = fieldSerializer.save()
						soil_ = request.data.get('soil')
						self.process_soil(soil_['method'], soil_['value'], field)
						self.process_irrigation_system(request.data.get('irr'), field)
						self.process_crop(request.data.get('plant'), field)
						logging.info('starting the process ....')
						task_id = process_new_field.delay(field.id, field.boundaries.wkt, field.boundaries[0][0])
						logger.info(task_id)
						return Response(task_id.id, status=status.HTTP_201_CREATED)
					except Exception as e:
						logger.error(f"Error occurred during data processing: {str(e)}")  # Log error
						return Response({"error": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

class Irrigation(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request):

		field_id	= request.data.get('field_id')
		amount 		= request.data.get('amount')
		date		= request.data.get('date')
		
		if field_id and amount and date:
			try :
				user = request.user
				irrigation = Irrigation_system.objects. \
								select_related('field_id').get(field_id=field_id,
								field_id__user_id=user.id)

				if irrigation != None:
					new_irr = Irrigation_amount(amount=amount, date=date,irrigation_system_id=irrigation)
					new_irr.save()
					return Response("Done !", status=status.HTTP_201_CREATED)
			
			except Exception as e:
				logger.error(f"Error occurred during data processing: {str(e)}")  # Log error
				return Response({f"error": "An error occurred while processing your request : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response("Error in Data", status=status.HTTP_400_BAD_REQUEST)

class check_pro(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]
	
	def post(self, request):

		task_id = request.query_params.get('task_id')
		result = AsyncResult(task_id)

		logger.info('heeey somttt')
		if result.ready():
			if result.successful():
				Response("Ok", status=status.HTTP_200_OK)
			else:
				Response(f"Error : {result.result}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else :
			Response("Task is still running")

