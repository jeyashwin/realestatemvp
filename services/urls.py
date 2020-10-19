from django.urls import path
from .views import *

app_name = "services"

urlpatterns = [
    path('services/', temp, name="servicesList"),
    # path('services/<int:pk>', ServicesDetailView.as_view(), name="servicesDetail"),
]
