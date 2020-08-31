from django.urls import path
from .views import *

urlpatterns = [
    path("property/",homepage),
    path("property-registration/",view_register),#shows the property registration page
    path("add-property",register_property),#adds the data to the database


]