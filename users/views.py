from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User

from .models import UserStudent, UserLandLord, UserType
from .forms import SignUpForm, LoginInForm, StudentProfileUpdateForm, LandlordProfileUpdateForm

# Create your views here.

#User App views starts from here

def Home(request):
    signUpFormIdentifier = SignUpForm(label_suffix='')
    LoginFormIdentifier = LoginInForm(label_suffix='')
    context = {
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
        
        # return JsonResponse({'success_message': "created"}, status=201)
        return redirect('user:home')

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
                    return redirect('user:home')

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


class StudentProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserStudent
    form_class = StudentProfileUpdateForm
    template_name = "templates/profile-user.html"

    def get_object(self):
        if self.request.user.username == self.kwargs.get('username'):
            return get_object_or_404(UserStudent, user__user__username=self.kwargs.get('username'))
        else:
            raise Http404
    
    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        studentUser = User.objects.get(username=self.request.user.username)
        studentUser.first_name = first_name
        studentUser.last_name = last_name
        studentUser.save()
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('user:studentProfile', kwargs={'username':self.kwargs.get('username')})


class LandlordProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserLandLord
    form_class = LandlordProfileUpdateForm
    template_name = "templates/profile-landlord.html"

    def get_object(self):
        if self.request.user.username == self.kwargs.get('username'):
            return get_object_or_404(UserLandLord, user__user__username=self.kwargs.get('username'))
        else:
            raise Http404
    
    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        landlordUser = User.objects.get(username=self.request.user.username)
        landlordUser.first_name = first_name
        landlordUser.last_name = last_name
        landlordUser.save()
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('user:landlordProfile', kwargs={'username':self.kwargs.get('username')})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "templates/profile-delete.html"
    slug_field = "url_slug"
    success_url = "/"

    def get_object(self):
        if self.request.user.username == self.kwargs.get('username'):
            return get_object_or_404(User, username=self.kwargs.get('username'))
        else:
            raise Http404

def Contact(request):
    return render(request, "templates/contact.html")

