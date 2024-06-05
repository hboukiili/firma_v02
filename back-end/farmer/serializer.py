from rest_framework import serializers
from models_only.models import *

def email_exists(email):
    return (Farmer.objects.filter(email=email).exists() or
            Searcher.objects.filter(email=email).exists() or
            PolicyMaker.objects.filter(email=email).exists())

class FarmerSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    
    class Meta:
        model = Farmer
        fields = ['first_name', 'last_name', 'email', 'password', 'test', 'type',]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data.pop('type')
        return Farmer.objects.create_user(**validated_data)
    
class loginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)

class FieldSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=20)
    boundaries = serializers.CharField(max_length=100)

class SoilSerializer(serializers.Serializer):

    pass

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['start_date', 'end_date', 'field_id']

    def create(self, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        field_id = validated_data.get('field_id')

        new_season = Season(
            start_date=start_date,
            end_date=end_date,
            field_id=field_id
        )
        new_season.save()
        return new_season