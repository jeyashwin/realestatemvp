from django.urls import path
from .views import *
from . import views

app_name = "services"

urlpatterns = [
    path('services/', ServiceListView.as_view(), name="servicesList"),
    path('services/<int:pk>', ServiceDetailView.as_view(), name="servicesDetail"),
    # path('services/serviceCreate', views.ServiceListCreate.as_view()),
    # path('services/serviceView', views.ServiceViewSet.as_view({'get': 'list'})),
    # path('services/imageCreate', views.ServiceImageListCreate.as_view()),
    # path('services/imageView', views.ServiceImageViewSet.as_view({'get': 'list'}))
]
