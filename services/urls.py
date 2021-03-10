from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
    path('services/', ServiceListView.as_view(), name="servicesList"),
    path('services/<int:pk>', ServiceDetailView.as_view(), name="servicesDetail"),
]
