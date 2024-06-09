from rest_framework import serializers

class Ogimet_Serializer(serializers.Serializer):
    
    field_id = serializers.IntegerField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    # band = serializers.CharField()
    # def validate(self, data):
    #     if data["test"] is not True:
    #         # print("here")
    #         raise serializers.ValidationError("Custom condition not met.")
    #     return super().validate(data)