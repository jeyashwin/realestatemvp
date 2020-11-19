from django.urls import path

from .views import *

app_name = "checkout"

urlpatterns = [
    path('property/<slug:slug>/request-to-rent/', RequestToRentPropertyCreateView, name="requestRent"),
    path('property/<slug:slug>/request-to-tour/', RequestToTourPropertyCreateView, name="requestTour"),
    path('services/<int:pk>/request-to-rent/', RequestToRentServiceCreateView, name="requestService"),
    path('myrequests/', myrequest, name="myrequest"),
    path('request/rent/<int:pk>/', RequestToRentPropertyDetailView.as_view(), name="rentRequestDetail"),
    path('request/tour/<int:pk>/', RequestToTourPropertyDetailView.as_view(), name="tourRequestDetail"),
]
