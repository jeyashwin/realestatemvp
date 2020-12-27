from django.shortcuts import render

from users.views import AuthenticationForm, LandlordSignupForm, StudentSignupForm, ForgotPasswordForm
# Create your views here.

def home(request):
    context = {
        "form" : AuthenticationForm(),
        "LandlordSignupForm" : LandlordSignupForm(label_suffix=''),
        "StudentSignupForm"  : StudentSignupForm(label_suffix=''),
        "ForgotPasswordForm" : ForgotPasswordForm(label_suffix=''),
    }
    return render(request, 'resources/home.html', context=context)