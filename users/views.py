from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, FormView
from django.http import JsonResponse

from .models import UserBuyer, UserLandLord
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
        form.instance.email = form.cleaned_data.get('email').lower()
        valid = super().form_valid(form)
        typeOfUser = form.cleaned_data.get('regUserType')
        if typeOfUser == "buyer":
            isCollegeStudent = False
            if form.cleaned_data.get('is_college_student'):
                isCollegeStudent = True
            if form.cleaned_data.get('college_name') == "":
                buyerObject = UserBuyer.objects.create(user=form.instance, isStudent=isCollegeStudent, 
                                    dateOfBirth=form.cleaned_data.get('date_of_birth'))
            else:
                buyerObject = UserBuyer.objects.create(user=form.instance, isStudent=isCollegeStudent, 
                                   collegeName=form.cleaned_data.get('college_name'), 
                                   dateOfBirth=form.cleaned_data.get('date_of_birth'))

        elif typeOfUser == "seller":
            landlordObject = UserLandLord.objects.create(user=form.instance, 
                                dateOfBirth=form.cleaned_data.get('date_of_birth'))
        
        return JsonResponse({'success_message': "created"}, status=200)

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
        userType = form.cleaned_data.get('logUserType')

        if userType == "buyer":
            try:
                user_exists = UserBuyer.objects.get(user__email=email)
            except UserBuyer.DoesNotExist:
                return JsonResponse({'user': 'Entered email and password does not match'}, status=404)
        elif userType == "seller":
            try:
                user_exists = UserLandLord.objects.get(user__email=email)
            except UserLandLord.DoesNotExist:
                return JsonResponse({'user': 'Entered email and password does not match'}, status=404)

        if user_exists:
            user = authenticate(username = user_exists.user.username, password = password)

            if user:
                if user.is_active:
                    login(self.request, user)
                    return redirect('user:sample')

                else:
                    return JsonResponse({'user': 'Account not active'}, status=400)
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