from django.urls import path
from .views import *

app_name = 'property'

urlpatterns = [
    path("add-comment",add_comment),#adds the data to the database
    path("property/", PropertyListView.as_view(), name="propertyList"),
    path("property/create", PropertyCreateView.as_view(), name="propertyCreate"),
    path("property/update/<slug:slug>", PropertyUpdateView.as_view(), name="propertyUpdate"),
    path("property/delete/<slug:slug>", PropertyDeleteView.as_view(), name="propertyDelete"),
    path("property/<int:pk>", PropertyDetailView.as_view(), name="detailedProperty"),
]