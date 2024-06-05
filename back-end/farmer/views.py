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

class register(APIView):

	permission_classes = [AllowAny]

	@swagger_auto_schema(
	    operation_description="register a new user",
	    request_body=openapi.Schema(
	        type=openapi.TYPE_OBJECT,
	        properties={
	            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
	            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
	            'password' : openapi.Schema(type=openapi.TYPE_STRING),
	            'email' : openapi.Schema(type=openapi.TYPE_STRING),
				'test' : openapi.Schema(type=openapi.TYPE_STRING),
				'type' : openapi.Schema(type=openapi.TYPE_STRING)
				
			},
	    ),
	)

	def post(self, request):

		if email_exists(request.data.get("email")):
			return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
		
		if request.data.get('type') != None:
			user_type = request.data.get('type')
		
		serializer = FarmerSerializer(data=request.data)
		if serializer.is_valid() :

			user = serializer.save()
			refresh = RefreshToken.for_user(user)
			refresh['user_type'] = user_type
			access_token = str(refresh.access_token)
			refresh_token = str(refresh)
			return Response({'access_token': access_token,
					'refresh_token': refresh_token}, status=status.HTTP_201_CREATED)

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
			
			user, user_type = get_user_by_email(email)
			if user is None:
				return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

			if not user.check_user_password(password):
				return Response({"message": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)

			refresh = RefreshToken.for_user(user)
			refresh['user_type'] = user_type

			return Response({
				'access_token': str(refresh.access_token),
				'refresh_token': str(refresh)
			}, status=status.HTTP_201_CREATED)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class field(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		
		user = request.user
		fields = Field.objects.filter(user_id=user.id)
		if fields.exists():
			fields_data = [{'id' : field.id, 'name': field.name, 'boundaries': field.boundaries} for field in fields]
			return Response(fields_data, status=status.HTTP_200_OK)
		return Response({"detail": "No fields found for this user."}, status=status.HTTP_404_NOT_FOUND)
	
	@swagger_auto_schema(
	    operation_description="create a new field",
	    request_body=openapi.Schema(
	        type=openapi.TYPE_OBJECT,
	        properties={
	            'name': openapi.Schema(type=openapi.TYPE_STRING),
	            'boundaries': openapi.Schema(type=openapi.TYPE_STRING),
			},
	    ),
	)
	def post(self, request):
		
		serializer = FieldSerializer(data=request.data)
		if serializer.is_valid():
			try:
				new_field = Field.objects.create(
					user_id=request.user, 
					name=serializer.validated_data.get('name'),
					boundaries=serializer.validated_data.get('boundaries')
				)
				new_field.save()
				return Response({"message": "Field created successfully"}, status=status.HTTP_201_CREATED)
			except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	@swagger_auto_schema(
	    operation_description="create a new field",
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

class season(APIView):

	authentication_classes = [FARMERJWTAuthentication]
	permission_classes = [IsAuthenticated]
	
	@swagger_auto_schema(
		manual_parameters=[
            openapi.Parameter('field_id', openapi.IN_QUERY, description="ID of the field", type=openapi.TYPE_INTEGER)
		],
		responses={200: SeasonSerializer(many=True)}
	)
	def get(self, request):
		field_id = request.query_params.get('field_id')
		
		if not field_id:
			return Response({"error": "Field ID is required"}, status=status.HTTP_400_BAD_REQUEST)

		seasons = Season.objects.filter(field_id=field_id)
		if seasons.exists():
			seasons_data = [{'id' : _season.id, 'start_date' : _season.start_date, 'end_date' : _season.end_date} for _season in seasons]
			return Response(seasons_data, status=status.HTTP_200_OK)
		return Response({"detail": "No Season found for this field."}, status=status.HTTP_404_NOT_FOUND)

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