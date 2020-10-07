from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User

from .models import UserStudent, UserLandLord, UserType
from .forms import *

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'index.html'

    def get_success_url(self):
        try:
            if self.request.user.usertype.is_student:
                return reverse_lazy('property:propertyList')
            else:
                return reverse_lazy('property:propertyManage')
        except:
            return reverse_lazy('user:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["LandlordSignupForm"] = LandlordSignupForm
        context["StudentSignupForm"] = StudentSignupForm
        return context


class LandlordSignUpView(CreateView):
    form_class = LandlordSignupForm
    success_url = "/"
    template_name = 'index.html'

    def form_valid(self, form):
        #creating new user with email (converting into lowercase)
        form.instance.email = form.cleaned_data.get('email').lower()
        valid = super().form_valid(form)
        userObject = UserType.objects.create(user=form.instance,
                        userType="seller")
        landlordObject = UserLandLord.objects.create(user=userObject, 
                            phone=form.cleaned_data.get('phone'),
                            profilePicture=form.cleaned_data.get('profilePicture'),
                        )
        return redirect('user:home')

    def form_invalid(self, form):
        invalid = super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def get(self, request):
        return redirect('user:home')


class StudentSignUpView(CreateView):
    form_class = StudentSignupForm
    success_url = "/"
    template_name = 'index.html'

    def form_valid(self, form):
        #creating new user with email (converting into lowercase)
        form.instance.email = form.cleaned_data.get('email').lower()
        valid = super().form_valid(form)
        interests=form.cleaned_data.get('interests')
        userObject = UserType.objects.create(user=form.instance,
                        userType="student")
        
        studentObject = UserStudent.objects.create(user=userObject, 
                            phone=form.cleaned_data.get('phone'),
                            university=form.cleaned_data.get('university'), 
                            classYear=form.cleaned_data.get('classYear'), 
                            bio=form.cleaned_data.get('bio'), 
                            profilePicture=form.cleaned_data.get('profilePicture')
                        )
        studentObject.interests.set(interests)

        return redirect('user:home')

    def form_invalid(self, form):
        invalid = super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def get(self, request):
        return redirect('user:home')


class StudentProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserStudent
    form_class = StudentProfileUpdateForm
    template_name = "users/profile-user.html"

    def get_object(self):
        if self.request.user.username == self.kwargs.get('username'):
            return get_object_or_404(UserStudent, user__user__username=self.kwargs.get('username'))
        else:
            raise Http404
    
    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email').lower()
        studentUser = User.objects.get(username=self.request.user.username)
        studentUser.first_name = first_name
        studentUser.last_name = last_name
        studentUser.email = email
        studentUser.save()
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('user:studentProfile', kwargs={'username':self.kwargs.get('username')})


class LandlordProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserLandLord
    form_class = LandlordProfileUpdateForm
    template_name = "users/profile-landlord.html"

    def get_object(self):
        if self.request.user.username == self.kwargs.get('username'):
            return get_object_or_404(UserLandLord, user__user__username=self.kwargs.get('username'))
        else:
            raise Http404
    
    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email').lower()
        landlordUser = User.objects.get(username=self.request.user.username)
        landlordUser.first_name = first_name
        landlordUser.last_name = last_name
        landlordUser.email = email
        landlordUser.save()
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('user:landlordProfile', kwargs={'username':self.kwargs.get('username')})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/profile-delete.html"
    success_url = "/"

    def get_object(self):
        if self.request.user.username == self.kwargs.get('username'):
            return get_object_or_404(User, username=self.kwargs.get('username'))
        else:
            raise Http404

def Contact(request):
    return render(request, "contact.html")

