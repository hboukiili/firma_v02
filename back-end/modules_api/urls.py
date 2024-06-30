from django.urls import path, include
from .views import *

urlpatterns = [
    path('ogimet', ogimet.as_view()),
    path('aquacrop', aquacrop.as_view())
]