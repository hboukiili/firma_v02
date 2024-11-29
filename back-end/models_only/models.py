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

class Crop(models.Model):

    Crop                = models.CharField(max_length=30, blank=True, null=True)
    Crop_planting_date  = models.DateField(blank=True, null=True)
    Tree                = models.CharField(max_length=30, blank=True, null=True)
    Tree_planting_date  = models.DateField(blank=True, null=True)
    field_id            = models.ForeignKey(Field, on_delete=models.CASCADE)


class Soil_type(Enum):

    SILT            = 'SILT'
    LOAMY_SAND      = 'LOAMY SAND'
    SAND            = 'SAND'
    SANDY_LOAM      = 'SANDY LOAM'
    LOAM            = 'LOAM'
    SANDY_CLAY_LOAM = 'SANDY CLAY LOAM'
    CLAY_LOAM       = 'CLAY LOAM'
    SILTY_CLAY      = 'SILTY CLAY'
    SANDY_CLAY      = 'SANDY CLAY'
    CLAY            = 'CLAY'

class soil_input(Enum):
    selection   = 'Selection'
    composition = 'Composition'
    satellite   = 'satellite'

class Soil(models.Model):

    soil_input_method   = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in soil_input])
    soil_type           = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in Soil_type], blank=True, null=True)
    sand_percentage     = models.IntegerField(blank=True, null=True)
    silt_percentage     = models.IntegerField(blank=True, null=True)
    clay_percentage     = models.IntegerField(blank=True, null=True)
    field_id            = models.ForeignKey(Field, on_delete=models.CASCADE)

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

    pass

class Drone (Data_source):

    pass

class Ogimet_stations(models.Model):

    station_id = models.IntegerField(blank=True, null=True)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    location_name = models.CharField(max_length=50)

class Irrigation_type(Enum):

    Sprinkler = 'Sprinkler irrigation'
    Surface   = 'Surface irrigation'
    Drip      = 'Drip irrigation'
    Rainfed   = 'Rainfed irrigation'

class Irrigation_system(models.Model):

    irrigation_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in Irrigation_type])
    instalation_date = models.DateField(blank=True, null=True)
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)

class Irrigation_amount(models.Model):

    amount = models.IntegerField()
    date = models.DateField()
    irrigation_system_id = models.ForeignKey(Irrigation_system, on_delete=models.CASCADE)

class Surface_irrigation(Irrigation_system):
    pass

class Sprinkler_irrigation(Irrigation_system):

    coverage_area = models.IntegerField(blank=True, null=True)
    outflow_rate = models.IntegerField(blank=True, null=True)
    number_of_sprinklers = models.IntegerField(blank=True, null=True)


class Drip_Irrigation(Irrigation_system):
    
    Crop_Tubes_distance     = models.IntegerField(blank=True, null=True)
    Crop_Drippers_distance  = models.IntegerField(blank=True, null=True)
    Crop_outflow_rate       = models.IntegerField(blank=True, null=True)    
    Tree_row_distance       = models.IntegerField(blank=True, null=True)
    Tree_distance           = models.IntegerField(blank=True, null=True)
    Tubes_number_by_tree    = models.IntegerField(blank=True, null=True)
    drippers_number_by_tree = models.IntegerField(blank=True, null=True)
    Tree_outflow_rate       = models.IntegerField(blank=True, null=True)    

class Maitenance_dates(models.Model):

    date = models.DateField()
    irrigation_system_id = models.ForeignKey(Irrigation_system, on_delete=models.CASCADE)


class Sol_Fao_Parametre(models.Model):

    sol = models.CharField(max_length=20)
    REW_min = models.FloatField(blank=True, null=True)
    REW_max = models.FloatField(blank=True, null=True)
    thetaFC_min = models.FloatField(blank=True, null=True)
    thetaFC_max = models.FloatField(blank=True, null=True)
    thetaWP_min = models.FloatField(blank=True, null=True)
    thetaWP_max = models.FloatField(blank=True, null=True)

class Fao_Crop_Parametre(models.Model):

    crop = models.CharField(max_length=20)
    Kcbini = models.FloatField(blank=True, null=True)
    Kcbmid = models.FloatField(blank=True, null=True)
    Kcbend = models.FloatField(blank=True, null=True)
    Lini = models.FloatField(blank=True, null=True)
    Ldev = models.FloatField(blank=True, null=True)
    Lmid = models.FloatField(blank=True, null=True)
    Lend = models.FloatField(blank=True, null=True)
    Zrini = models.FloatField(default=0.05)
    zrmax = models.FloatField(blank=True, null=True)
    pbase = models.FloatField(blank=True, null=True)
    Ze = models.FloatField(default=0.10)

class fao_output(models.Model):

    field   = models.ForeignKey(Field, on_delete=models.CASCADE)
    date    = models.DateField(blank=True, null=True)
    kcb     = gis.RasterField()
    fc      = gis.RasterField()
    DB      = gis.RasterField()
    E       = gis.RasterField()
    ETcadj  = gis.RasterField()
    ETref   = gis.RasterField()
    Irrig   = gis.RasterField()
    Kcadj   = gis.RasterField()
    Ks      = gis.RasterField()
    Rain    = gis.RasterField()
    Runoff  = gis.RasterField()
    T       = gis.RasterField()
    Zr      = gis.RasterField()

class Sentinel2(models.Model):

    path = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)

class Weather_date(models.Model):

    Date        = models.DateTimeField(blank=True, null=True)
    Field_id    = models.ForeignKey(Field, on_delete=models.CASCADE)
    T2m         = models.FloatField(blank=True, null=True)
    Ws          = models.FloatField(blank=True, null=True)
    Et0         = models.FloatField(blank=True, null=True)
    Rain        = models.FloatField(blank=True, null=True)
    Rh          = models.FloatField(blank=True, null=True)
    D2m         = models.FloatField(blank=True, null=True)


class forcast_Weather_date(models.Model):

    Date        = models.DateTimeField(blank=True, null=True)
    Field_id    = models.ForeignKey(Field, on_delete=models.CASCADE)
    T2m         = models.FloatField(blank=True, null=True)
    Ws          = models.FloatField(blank=True, null=True)
    Et0         = models.FloatField(blank=True, null=True)
    Rain        = models.FloatField(blank=True, null=True)
    Rh          = models.FloatField(blank=True, null=True)
    D2m         = models.FloatField(blank=True, null=True)

class aquacrop_output(models.Model):
    
    date = models.DateField(blank=True, null=True)
    field_id = models.ForeignKey(Field, on_delete=models.CASCADE)
    IrrDay     = models.FloatField()
    Tr =        models.FloatField()
    DeepPerc =  models.FloatField()
    Es  =       models.FloatField()
    Th1 =       models.FloatField()
    Th2 =       models.FloatField()
    th3 =       models.FloatField()
    gdd_cum = models.FloatField()
    canopy_cover = models.FloatField()
    biomass =models.FloatField()
    z_root =models.FloatField()
    DryYield =models.FloatField()
    FreshYield =models.FloatField()
    harvest_index = models.FloatField()
    ET = models.FloatField()