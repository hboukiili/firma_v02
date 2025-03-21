from django.urls import path, include
from .views import *

urlpatterns = [
    path('ogimet', ogimet.as_view()),
    path('aquacrop', aquacrop.as_view()),
    path('fao_test', FaoTest.as_view()),
    path('current_weather', current_weather.as_view()),
    path('weather', weather.as_view()),
    path('forcast', Forcast.as_view()),
    path('gdd', gdd.as_view()),
]