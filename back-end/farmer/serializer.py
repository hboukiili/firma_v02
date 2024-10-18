from rest_framework import serializers
from models_only.models import *
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
import json
from django.contrib.gis.geos import GEOSGeometry


class GeoJSONStringField(serializers.Field):
    def to_internal_value(self, data):
        try:
            # Parse the string to a JSON object
            geojson = json.loads(data)
            # Extract the geometry part from the GeoJSON FeatureCollection
            geometry = geojson['geometry']
            # Convert the geometry JSON object to a GEOSGeometry object
            return GEOSGeometry(json.dumps(geometry))
        except (TypeError, ValueError, KeyError) as e:
            raise serializers.ValidationError(f"Invalid GeoJSON: {str(e)}")

    def to_representation(self, value):
        # Convert the GEOSGeometry object to GeoJSON string
        return value.json

def email_exists(email):
    return (Farmer.objects.filter(email=email).exists() or
            Searcher.objects.filter(email=email).exists() or
            PolicyMaker.objects.filter(email=email).exists())

class FarmerSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    
    class Meta:
        model = Farmer
        fields = ['first_name', 'last_name', 'email', 'password', 'type',]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        validated_data.pop('type')
        return Farmer.objects.create_user(**validated_data)
    
class loginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)

class FieldSerializer(GeoFeatureModelSerializer):
    boundaries = GeoJSONStringField()

    class Meta:
        model = Field
        fields = ('id', 'name', 'boundaries')
        geo_field = 'boundaries'

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

class SoilSerializer(serializers.Serializer):

    pass

# class SeasonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Season
#         fields = ['start_date', 'end_date', 'field_id']

#     def create(self, validated_data):
#         start_date = validated_data.get('start_date')
#         end_date = validated_data.get('end_date')
#         field_id = validated_data.get('field_id')

#         new_season = Season(
#             start_date=start_date,
#             end_date=end_date,
#             field_id=field_id
#         )
#         new_season.save()
#         return new_season