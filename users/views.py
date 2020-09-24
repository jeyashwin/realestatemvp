from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView
from django.http import JsonResponse

from .models import UserStudent, UserLandLord, UserType
from .forms import SignUpForm, LoginInForm

# Create your views here.

def decoding(obj):
    return eval(obj.decode())

#User App views starts from here

def Home(request):
    signUpFormIdentifier = SignUpForm(label_suffix='')
    LoginFormIdentifier = LoginInForm(label_suffix='')
    context = {
        "status" : 0, 
        'SignUpform': signUpFormIdentifier, 
        'Loginform': LoginFormIdentifier,
    }
    return render(request, "templates/index.html", context=context )

class SignUpClassView(CreateView):
    form_class = SignUpForm
    success_url = '/'
    template_name = "templates/index.html"
    
    def form_valid(self, form):

        #creating new user with email (converting into lowercase)
        form.instance.email = form.cleaned_data.get('email').lower()
        valid = super().form_valid(form)

        #creating new userType with user instance
        userObject = UserType.objects.create(user=form.instance,
                        userType=form.cleaned_data.get('regUserType'))

        if userObject.is_student:
            studentObject = UserStudent.objects.create(user=userObject, 
                                isCollegeStudent=form.cleaned_data.get('is_college_student'), 
                                collegeName=form.cleaned_data.get('college_name'), 
                                dateOfBirth=form.cleaned_data.get('date_of_birth')
                            )

        if userObject.is_landlord:
            landlordObject = UserLandLord.objects.create(user=userObject, 
                                dateOfBirth=form.cleaned_data.get('date_of_birth'))
        
        return JsonResponse({'success_message': "created"}, status=201)

    def form_invalid(self, form):
        invalid = super().form_invalid(form)
        return JsonResponse(form.errors, status=400)
    
    def get(self, request):
        return redirect('user:home')
    

class UserLoginClassView(FormView):
    form_class = LoginInForm
    success_url = "/"
    template_name = "templates/index.html"

    def form_valid(self, form):
        valid = super().form_valid(form)
        email = form.cleaned_data.get('login_email').lower()
        password = form.cleaned_data.get('login_password')

        try:
            userExists = UserType.objects.get(user__email=email, 
                            userType=form.cleaned_data.get('logUserType'))
        except UserType.DoesNotExist:
            return JsonResponse({'user': 'Account not found'}, status=404)

        if userExists:
            user = authenticate(username = userExists.user.username, password = password)

            if user:
                if user.is_active:
                    login(self.request, user)
                    return redirect('user:sample')

                else:
                    return JsonResponse({'user': 'Account not active'}, status=403)
            else:
                return JsonResponse({'user': 'Invalid login details supplied!'}, status=404)

        return redirect('user:home')

    def form_invalid(self, form):
        invalid = super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def get(self, request):
        return redirect('user:home')


def sample(request):
    return render(request, "templates/sample.html")