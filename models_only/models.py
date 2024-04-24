from django.db import models
from enum import Enum

class users(models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)

class Agriculture(users):

    test = models.CharField(max_length=50)

class chercheur(users):

    test = models.CharField(max_length=30)

class Policy_Maker(users):

    test = models.CharField(max_length=30)

class field(models.Model):

    user_id = models.ForeignKey(users, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    boundaries = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

class saison(models.Model):

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    field_id = models.ForeignKey(field, on_delete=models.CASCADE)
    rendement = models.IntegerField()

class Crop(models.Model):

    crop_type = models.CharField(max_length=30)
    vatiety = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    saison_id = models.ForeignKey(saison, on_delete=models.CASCADE)

class Pratique_Agricole(models.Model):

    types = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_fin = models.DateField()
    quantite = models.IntegerField()
    crop_id = models.ForeignKey(Crop, on_delete=models.CASCADE)

class Soil_type(Enum):

    Loam = "Loam"
    Sandy = "Sandy soil"
    Clay = "Clay"
    Silty = "Silty"
    Peat = "Peat soil"
    Black = "Black soil"
    Arid = "Arid soil"

class soil(models.Model):

    soil_type = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in Soil_type])
    field_id = models.ForeignKey(field, on_delete=models.CASCADE)

class irrigation_system(models.Model):

    irrigation_type = models.CharField(max_length=50) # should be enum
    debit = models.IntegerField()
    instalation_date = models.DateField()
    Maintenance_date = models.DateField()
    field_id = models.ForeignKey(field, on_delete=models.CASCADE)

class Data_source(models.Model):

    datetime = models.DateField()
    field_id = models.ForeignKey(field, on_delete=models.CASCADE)

class Remote_sensing(Data_source):

    path = models.CharField(max_length=50)
    RS_type = models.CharField(max_length=50)
    source = models.CharField(max_length=50)

class station(Data_source):

    coordinates = models.CharField(max_length=50)
    station_type = models.CharField(max_length=20) # should be enum
    sensor_type = models.CharField(max_length=20) # should be enum
    mesur = models.IntegerField()

class Ogimet_stations(models.Model):

    id = models.IntegerField()
    coordinates = models.CharField()
    location_name = models.CharField()