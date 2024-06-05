from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(users)
admin.site.register(Farmer)
admin.site.register(Searcher)
admin.site.register(PolicyMaker)
admin.site.register(Field)
admin.site.register(Season)
admin.site.register(Crop)
admin.site.register(Soil)
admin.site.register(Remote_sensing)
admin.site.register(Station)
admin.site.register(Ogimet_stations)
admin.site.register(Soil_analysis)
admin.site.register(Maitenance_dates)