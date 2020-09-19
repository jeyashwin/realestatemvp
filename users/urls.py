from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

app_name = "user"

urlpatterns = [
    path('', Home, name='home'),
    path('register/', SignUpClassView.as_view(), name="signup"),
    path('login/', UserLoginClassView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name = "logout"),
    path('sample/', sample, name="sample")
]