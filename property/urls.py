from django.urls import path
from .views import *

app_name = 'property'

urlpatterns = [
    path("property-registration/",view_register),#shows the property registration page
    path("add-property",register_property),#adds the data to the database
    path("single-property",test_single),#adds the data to the database
    path("add-comment",add_comment),#adds the data to the database
    path("property/", PropertyListView.as_view(), name="propertyList"),
    path("property/<int:pk>", PropertyDetailView.as_view(), name="detailedProperty"),
]