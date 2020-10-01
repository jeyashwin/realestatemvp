from django.urls import path
from .views import *

app_name = 'students'

urlpatterns = [
    path('favourites/', favourites, name="favourites"),
    path('roommates/', roommates, name="roommates"),
]
