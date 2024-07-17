from django.urls import path, include
from .views import *

urlpatterns = [
    path('register', register.as_view()),
    path('login', login.as_view()),
    path('field', field.as_view()),
    # path('seasons/', season.as_view(), name='seasons_list'),
    path('register_data', register_data.as_view())
]