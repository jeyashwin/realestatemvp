from django.urls import path, include
from .views import *
from . import views

app_name = 'resources'

urlpatterns = [
    path('resources/', views.home, name="resources-home")
]