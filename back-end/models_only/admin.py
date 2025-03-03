from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Farmer)
# admin.site.register(Searcher)
# admin.site.register(PolicyMaker)
admin.site.register(Field)
admin.site.register(User)
admin.site.register(Crop)
admin.site.register(Soil)
admin.site.register(Remote_sensing)
admin.site.register(Station)
admin.site.register(Ogimet_stations)
admin.site.register(Maitenance_dates)
admin.site.register(Sprinkler_irrigation)
admin.site.register(Drip_Irrigation)
admin.site.register(Surface_irrigation)
admin.site.register(Irrigation_system)
admin.site.register(Irrigation_amount)
admin.site.register(Sol_Fao_Parametre)
admin.site.register(Fao_Crop_Parametre)
admin.site.register(Soil_analysis)