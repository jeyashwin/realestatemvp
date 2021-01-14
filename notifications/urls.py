from django.urls import path

from .views import *

app_name = 'notification'

urlpatterns = [
    path('notification/<int:pk>/', notification, name="notificationRedirect")   
]
