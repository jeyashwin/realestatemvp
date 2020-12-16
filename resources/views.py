from django.shortcuts import render


from users.views import AuthenticationForm, LandlordSignupForm, StudentSignupForm, ForgotPasswordForm
# Create your views here.

def home(request):
    value = signing.dumps('Aravindhan@123', key=settings.SECRET_KEY)
    print(value)
    print(signing.loads(value))
    context = {
        "form" : AuthenticationForm(),
        "LandlordSignupForm" : LandlordSignupForm(label_suffix=''),
        "StudentSignupForm"  : StudentSignupForm(label_suffix=''),
        "ForgotPasswordForm" : ForgotPasswordForm(label_suffix=''),
    }
    return render(request, 'resources/home.html', context=context)