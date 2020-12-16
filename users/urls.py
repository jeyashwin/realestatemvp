from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

app_name = "user"

urlpatterns = [
    path('', CustomLoginView.as_view(), name="home"),
    path('landlord/register/', LandlordSignUpView.as_view(), name="landlordSignup"),
    path('student/register/', StudentSignUpView.as_view(), name="studentSignup"),
    path('logout/', LogoutView.as_view(), name = "logout"),
    path('student/profile/<str:username>/', StudentProfileUpdateView.as_view(), name = "studentProfile"),
    path('student/livingHabits/', StudentLivingHabitsUpdateView, name = "studentLiving"),
    path('landlord/profile/<str:username>/', LandlordProfileUpdateView.as_view(), name = "landlordProfile"),
    path('delete/profile/<str:username>/', UserDeleteView.as_view(), name = "deleteProfile"),
    path('contact/', ContactUSCreateView.as_view(), name = "contactUs"),
    path('forgot-password/', ForgotPasswordView, name="forgotPass"),
    path('forgot-password/auth/change/', ForgotSetPassword, name="setPass"),
    path('verify/', otpverify, name="verifyPhone"),
    path('update/phone/', PhoneNumberUpdate, name="updatePhone"),
    path('resend/code/<int:pk>/', ResendVerificationCode, name="resendCode"),
]