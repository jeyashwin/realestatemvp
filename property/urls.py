from django.urls import path
from .views import *


urlpatterns = [
    path("property/",homepage,name='homepage'),
    path("property-registration/",view_register,),#shows the property registration page
    path("add-property",register_property),#adds the data to the database
    path("single-property",test_single),#adds the data to the database
    path("add-comment",add_comment),#adds the data to the database
    path('login',login, name='login'),
    path('like/<int:pk>/',likeView,name='like_prop'),
]