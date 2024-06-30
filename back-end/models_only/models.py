from django.db import models
from enum import Enum
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password
from django.contrib.gis.db import models as gis


class UserManager(models.Manager):
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = email.lower()
        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user


class users(models.Model):
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    username = None

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True

    def check_user_password(self, raw_password):
        return check_password(raw_password, self.password)

class farmermanager(UserManager):
    pass

class Farmer(users):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']    
    class Meta:
        verbose_name = ('farmer')
        verbose_name_plural = ('farmers')

    objects = farmermanager()

class SearcherManager(UserManager):
    pass

class Searcher(users):

    objects = SearcherManager()

class PolicyMakerManager(UserManager):
    pass

class PolicyMaker(users):

    objects = PolicyMakerManager()

class Field(models.Model):

    user_id = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    boundaries = gis.PolygonField()

class Season(models.Model):

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)

# class Season(models.Model):
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)

# class Field(models.Model):

#     user_id = models.ForeignKey(Farmer, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#     boundaries = gis.PolygonField()
#     saison_id = models.ForeignKey(Season, on_delete=models.CASCADE)

class Crop(models.Model):

    crop_type = models.CharField(max_length=30)
    vatiety = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    saison_id = models.ForeignKey(Season, on_delete=models.CASCADE)

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

class Soil(models.Model):

    soil_type = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in Soil_type])
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)

class Soil_analysis(models.Model):

    soil_id = models.ForeignKey(Soil, on_delete=models.CASCADE)
    PH_eau = models.FloatField()
    EC_ms_cm = models.FloatField()
    EC_ms_cm_pate_saturée = models.FloatField()
    Argile = models.FloatField()
    Limon = models.FloatField()
    Sable = models.FloatField()
    MO = models.FloatField()
    Nt = models.FloatField()
    P205 = models.FloatField()
    K20 = models.FloatField()
    Na20 = models.FloatField()
    Na = models.FloatField()
    Cao = models.FloatField()
    Ca = models.FloatField()
    MGo = models.FloatField()
    Mg = models.FloatField()
    SAR = models.FloatField()
    Cu = models.FloatField()
    Mn = models.FloatField()
    Fe = models.FloatField()
    Zn = models.FloatField()
    NNH4 = models.FloatField()
    NO3 = models.FloatField()
    CI = models.FloatField()
    BORE = models.FloatField()
    Caco3 = models.FloatField()
    Caco3_actif_AXB = models.FloatField() 

class Irrigation_system(models.Model):

    irrigation_type = models.CharField(max_length=50) # should be enum
    debit = models.IntegerField()
    instalation_date = models.DateField()
    Maintenance_date = models.DateField()
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)

class Maitenance_dates(models.Model):

    date = models.DateField()
    irrigation_system_id = models.ForeignKey(Irrigation_system, on_delete=models.CASCADE)

class Data_source(models.Model):
    datetime = models.DateField(blank=True, null=True)
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

class Remote_sensing(Data_source):

    path = models.CharField(max_length=50)
    RS_type = models.CharField(max_length=50)
    source = models.CharField(max_length=50)

class Station(Data_source):

    coordinates = models.CharField(max_length=50)
    station_type = models.CharField(max_length=20) # should be enum
    sensor_type = models.CharField(max_length=20) # should be enum
    mesur = models.IntegerField()

class Lidar(Data_source):

    test = models.CharField(max_length=20)

class Drone (Data_source):

    test = models.CharField(max_length=20)

class Ogimet_stations(models.Model):

    station_id = models.IntegerField(blank=True, null=True)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    location_name = models.CharField(max_length=50)

