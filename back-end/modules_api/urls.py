from django.urls import path, include
from .views import *

urlpatterns = [
    path('ogimet', ogimet.as_view()),
    path('aquacrop', aquacrop.as_view()),
    path('fao_test', fao_test.as_view()),
    path('current_weather', current_weather.as_view()),
]