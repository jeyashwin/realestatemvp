from django.urls import path
from .views import *

app_name = 'students'

urlpatterns = [
    path('favourites/', FavouriteListView.as_view(), name="favourites"),
    path('favourites/add/<slug:slug>/', AddFavourite, name="addFavourites"),
    path('favourites/remove/<slug:slug>/', RemoveFavourite, name="removeFavourites"),
    path('roommates/', roommates, name="roommates"),
]
