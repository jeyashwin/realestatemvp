from django.urls import path
from .views import *


urlpatterns = [
    path("property/",homepage,name='homepage'),
    path("property-registration/",view_register,),#shows the property registration page
    path("add-property",register_property),#adds the data to the database
    path("single-property",test_single,name='coment'),#adds the data to the database
    path("add-comment/<property_id>/",add_comment,name='coment_add'),#adds the data to the database
    path('login',login),
    path('update_property/<pid>',update_property)
    # path('like/<int:pk>/',likeView,name='like_prop'),
]