from django.urls import path

from .views import *

app_name = "checkout"

urlpatterns = [
    path('property/<slug:slug>/request-to-rent/', RequestToRentPropertyCreateView, name="requestRent"),
    path('services/<int:pk>/request-to-rent/', RequestToRentServiceCreateView, name="requestService"),
]
