from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User

from .models import UserStudent, UserLandLord, UserType, InviteCode, ContactUS
from .forms import *

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'index.html'

    # def form_valid(self, form):
    #     """Security check complete. Log the user in."""
    #     user = form.get_user()
    #     if not user.is_superuser and not user.is_staff:
    #         if user.usertype.is_student:
    #             if user.usertype.userstudent.phoneVerified:
    #                 auth_login(self.request, form.get_user())
    #                 return HttpResponseRedirect(self.get_success_url())
    #             else:
    #                 return JsonResponse({'failed': 'not again student'})
    #         else:
    #             if user.usertype.userlandlord.phoneVerified:
    #                 auth_login(self.request, form.get_user())
    #                 return HttpResponseRedirect(self.get_success_url())
    #             else:
    #                 return JsonResponse({'failed': 'not again'})
    #     else:
    #         auth_login(self.request, form.get_user())
    #         return HttpResponseRedirect(self.get_success_url())

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
        context["LandlordSignupForm"] = LandlordSignupForm(label_suffix='')
        context["StudentSignupForm"] = StudentSignupForm(label_suffix='')
        context["ForgotPasswordForm"] = ForgotPasswordForm(label_suffix='')
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
                            profilePicture=form.cleaned_data.get('lanprofilePicture'),
                        )
        messages.add_message(self.request, messages.SUCCESS, 'Landlord Profile created successfully. Sign in to you account.')
        return redirect('user:home')

    def form_invalid(self, form):
        invalid = super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def get(self, request):
        return redirect('user:home')


def get_or_create_interest(tempInterest):
    tempInterest = tempInterest.capitalize()
    # print(tempInterest)
    return Interest.objects.get_or_create(interest=tempInterest)


class StudentSignUpView(CreateView):
    form_class = StudentSignupForm
    success_url = "/"
    template_name = 'index.html'

    def form_valid(self, form):
        #creating new user with email (converting into lowercase)
        form.instance.email = form.cleaned_data.get('email').lower()
        valid = super().form_valid(form)
        # interests=form.cleaned_data.get('interests')
        interest1 = get_or_create_interest(form.cleaned_data.get('interest1'))
        interest2 = get_or_create_interest(form.cleaned_data.get('interest2'))
        interest3 = get_or_create_interest(form.cleaned_data.get('interest3'))
        

        userObject = UserType.objects.create(user=form.instance,
                        userType="student")
        
        studentObject = UserStudent.objects.create(user=userObject, 
                            phone=form.cleaned_data.get('phone'),
                            university=form.cleaned_data.get('university'), 
                            classYear=form.cleaned_data.get('classYear'), 
                            bio=form.cleaned_data.get('bio'), 
                            profilePicture=form.cleaned_data.get('profilePicture'),
                            fbLink=form.cleaned_data.get('fblink'),
                            snapLink=form.cleaned_data.get('snapLink'),
                            instaLink=form.cleaned_data.get('instaLink'),
                            twitterLink=form.cleaned_data.get('twitterLink'),
                            sleepScheduleFrom=form.cleaned_data.get('ssFrom'),
                            sleepScheduleTo=form.cleaned_data.get('ssTo'),
                            studyHourFrom=form.cleaned_data.get('shFrom'),
                            studyHourTo=form.cleaned_data.get('shTo'),
                            tobaccoUsage=form.cleaned_data.get('tbUsage'),
                            alcoholUsage=form.cleaned_data.get('alUsage'),
                            cleanliness=form.cleaned_data.get('cleanliness'),
                            guests=form.cleaned_data.get('guests'),
                        )
        # studentObject.interests.set(interests)
        studentObject.interests.set([interest1[0].pk, interest2[0].pk, interest3[0].pk])
        studentObject.save()

        inviteCode = self.request.GET.get('invite_code', None)
        if inviteCode:
            try:
                newUser = InviteCode.objects.get(inviteCode=inviteCode)
                newUser.studentJoined.add(studentObject)
                newUser.save()
            except InviteCode.DoesNotExist:
                print("Invite codes doesn't match! Ask your friend to resend.")
        
        messages.add_message(self.request, messages.SUCCESS, 'Student Profile created successfully. Sign in to you account.')
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
        valid = super().form_valid(form)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email').lower()
        interest1 = get_or_create_interest(form.cleaned_data.get('interest1'))
        interest2 = get_or_create_interest(form.cleaned_data.get('interest2'))
        interest3 = get_or_create_interest(form.cleaned_data.get('interest3'))
        form.instance.interests.set([interest1[0].pk, interest2[0].pk, interest3[0].pk])
        # form.save()
        studentUser = User.objects.get(username=self.request.user.username)
        studentUser.first_name = first_name
        studentUser.last_name = last_name
        studentUser.email = email
        studentUser.save()
        return valid
    
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


class ContactUSCreateView(CreateView):
    model = ContactUS
    template_name = "users/contact.html"
    form_class = ContactUSForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contactusform"] = context["form"]
        context["form"] = AuthenticationForm
        context["LandlordSignupForm"] = LandlordSignupForm(label_suffix='')
        context["StudentSignupForm"] = StudentSignupForm(label_suffix='')
        context["ForgotPasswordForm"] = ForgotPasswordForm(label_suffix='')
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('user:contactUs')

def ForgotPasswordView(request):

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('new_password1')
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
        else:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors.get(error), extra_tags='forgotPassword')
            # return JsonResponse(form.errors, status=400)

    return redirect('user:home')

def otpverify(request):
    context = {
        "form" : AuthenticationForm(),
        "LandlordSignupForm" : LandlordSignupForm(label_suffix=''),
        "StudentSignupForm"  : StudentSignupForm(label_suffix=''),
        "ForgotPasswordForm" : ForgotPasswordForm(label_suffix=''),
    }
    return render(request, 'users/verificationCode.html', context=context)