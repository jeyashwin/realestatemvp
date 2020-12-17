from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from twilio.rest import Client

from .models import UserStudent, UserLandLord, UserType, InviteCode, ContactUS, PhoneVerification
from .forms import *
from property.utils import studentAccessTest
import datetime

# Create your views here.

twilioClient = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

class CustomLoginView(LoginView):
    template_name = 'index.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        if not user.is_superuser and not user.is_staff:
            phone_verify = self.request.session.get('phone_verify', None)
            update_phone_verify = self.request.session.get('update_phone_verify', None)
            forgot_phone_verify = self.request.session.get('forgot_phone_verify', None)
            if phone_verify:
                del self.request.session['phone_verify']
            if update_phone_verify:
                del self.request.session['update_phone_verify']
            if forgot_phone_verify:
                del self.request.session['forgot_phone_verify']
            if user.usertype.is_student:
                if user.usertype.userstudent.phoneVerified:
                    if PhoneVerification.objects.filter(userObj=user).exists():
                        PhoneVerification.objects.get(userObj=user).delete()
                    auth_login(self.request, form.get_user())
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    if PhoneVerification.objects.filter(userObj=user).exists():
                        phonObj = PhoneVerification.objects.get(userObj=user)
                        if (phonObj.updatedDate < (timezone.now() - timezone.timedelta(minutes=10))):
                            phonObj.delete()
                        else:
                            self.request.session['phone_verify'] = user.username
                            return redirect('user:verifyPhone')
                    self.request.session['phone_verify'] = user.username
                    code = send_verfication_code(to=user.usertype.userstudent.phone)
                    return redirect('user:verifyPhone')
            else:
                if user.usertype.userlandlord.phoneVerified:
                    if PhoneVerification.objects.filter(userObj=user).exists():
                        PhoneVerification.objects.get(userObj=user).delete()
                    auth_login(self.request, form.get_user())
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    if PhoneVerification.objects.filter(userObj=user).exists():
                        phonObj = PhoneVerification.objects.get(userObj=user)
                        if (phonObj.updatedDate < (timezone.now() - timezone.timedelta(minutes=10))):
                            phonObj.delete()
                        else:
                            self.request.session['phone_verify'] = user.username
                            return redirect('user:verifyPhone')
                    self.request.session['phone_verify'] = user.username
                    code = send_verfication_code(to=user.usertype.userlandlord.phone)
                    return redirect('user:verifyPhone')
        else:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())

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

    def get(self, request):
        if request.user.is_authenticated:
            try:
                if request.user.usertype.is_student:
                    return redirect('property:propertyList')
                else:
                    return redirect('property:propertyManage')
            except:
                pass
        return super().get(self, request)


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
        profileImage = form.cleaned_data.get('lanprofilePicture', None)
        if not profileImage:
            profileImage = 'uploads/avatar/profile_avatar.png'
        landlordObject = UserLandLord.objects.create(user=userObject, 
                            phone=form.cleaned_data.get('phone'),
                            profilePicture=profileImage,
                        )
        # messages.add_message(self.request, messages.SUCCESS, 'Landlord/Sublease Profile created successfully. Sign in to you account.')
        # return redirect('user:home')
        return JsonResponse({'success':'Landlord/Sublease Profile created successfully. Sign in to you account.'}, status=201)

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
        profileImage = form.cleaned_data.get('profilePicture', None)
        if not profileImage:
            profileImage = 'uploads/avatar/profile_avatar.png'
        studentObject = UserStudent.objects.create(user=userObject, 
                            phone=form.cleaned_data.get('phone'),
                            university=form.cleaned_data.get('university'), 
                            classYear=form.cleaned_data.get('classYear'), 
                            # bio=form.cleaned_data.get('bio'),
                            profilePicture=profileImage,
                            fbLink=form.cleaned_data.get('fblink'),
                            # snapLink=form.cleaned_data.get('snapLink'),
                            instaLink=form.cleaned_data.get('instaLink'),
                            # twitterLink=form.cleaned_data.get('twitterLink'),
                            # sleepScheduleFrom=form.cleaned_data.get('ssFrom'),
                            # sleepScheduleTo=form.cleaned_data.get('ssTo'),
                            # studyHourFrom=form.cleaned_data.get('shFrom'),
                            # studyHourTo=form.cleaned_data.get('shTo'),
                            # tobaccoUsage=form.cleaned_data.get('tbUsage'),
                            # alcoholUsage=form.cleaned_data.get('alUsage'),
                            # cleanliness=form.cleaned_data.get('cleanliness'),
                            # guests=form.cleaned_data.get('guests'),
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
        
        # messages.add_message(self.request, messages.SUCCESS, 'Student Profile created successfully. Sign in to you account.')
        # return redirect('user:home')
        return JsonResponse({'success':'Student Profile created successfully. Sign in to you account.'}, status=201)

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
        phoneNumber = form.cleaned_data.get('Updatephone')
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
        if self.object.phone != phoneNumber:
            phoneVeriObj = PhoneVerification.objects.get_or_create(userObj=self.request.user)
            if phoneVeriObj[1]:
                phoneVeriObj[0].phone = phoneNumber
                phoneVeriObj[0].save()
                code = send_verfication_code(to=phoneNumber)
            else:
                if not phoneVeriObj[0].is_blocked or (phoneVeriObj[0].is_blocked and (phoneVeriObj[0].updatedDate < (timezone.now() - timezone.timedelta(minutes=10)))):
                    if phoneVeriObj[0].is_blocked:
                        code = send_verfication_code(to=phoneNumber)
                        phoneVeriObj[0].is_blocked = False
                        phoneVeriObj[0].phone = phoneNumber
                        phoneVeriObj[0].wrongAttemptCount = 5
                        phoneVeriObj[0].resendCodeCount = 3
                    else:
                        if phoneVeriObj[0].phone != phoneNumber:
                            code = send_verfication_code(to=phoneNumber)
                            phoneVeriObj[0].phone = phoneNumber
                            phoneVeriObj[0].wrongAttemptCount = 5
                            phoneVeriObj[0].resendCodeCount = 3
                    phoneVeriObj[0].save()
            self.request.session['update_phone_verify'] = 'student'
            return redirect('user:verifyPhone')
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
        phoneNumber = form.cleaned_data.get('Updatephone')
        landlordUser = User.objects.get(username=self.request.user.username)
        landlordUser.first_name = first_name
        landlordUser.last_name = last_name
        landlordUser.email = email
        landlordUser.save()
        valid = super().form_valid(form)
        if self.object.phone != phoneNumber:
            phoneVeriObj = PhoneVerification.objects.get_or_create(userObj=self.request.user)
            if phoneVeriObj[1]:
                phoneVeriObj[0].phone = phoneNumber
                phoneVeriObj[0].save()
                code = send_verfication_code(to=phoneNumber)
            else:
                if not phoneVeriObj[0].is_blocked or (phoneVeriObj[0].is_blocked and (phoneVeriObj[0].updatedDate < (timezone.now() - timezone.timedelta(minutes=10)))):
                    if phoneVeriObj[0].is_blocked:
                        code = send_verfication_code(to=phoneNumber)
                        phoneVeriObj[0].is_blocked = False
                        phoneVeriObj[0].phone = phoneNumber
                        phoneVeriObj[0].wrongAttemptCount = 5
                        phoneVeriObj[0].resendCodeCount = 3
                    else:
                        if phoneVeriObj[0].phone != phoneNumber:
                            code = send_verfication_code(to=phoneNumber)
                            phoneVeriObj[0].phone = phoneNumber
                            phoneVeriObj[0].wrongAttemptCount = 5
                            phoneVeriObj[0].resendCodeCount = 3
                    phoneVeriObj[0].save()
            self.request.session['update_phone_verify'] = 'landlord'
            return redirect('user:verifyPhone')
        return valid
    
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


def send_verfication_code(to, channel='sms'):
    try:
        verification = twilioClient.verify \
        .services(settings.TWILIO_VERIFICATION_SID) \
        .verifications \
        .create(to=phonenumbers.format_number(to, phonenumbers.PhoneNumberFormat.E164), channel=channel)
        # print(verification.sid)
        return verification.sid
    except Exception as e:
        print("Error validating code: {}".format(e))
        return False

def check_verification_code(phone, code):
    try:
        verification_check = twilioClient.verify \
            .services(settings.TWILIO_VERIFICATION_SID) \
            .verification_checks \
            .create(to=phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164), code=code)
        # print(verification_check.status)
        if verification_check.status == "approved":
            return True
        else:
            return False
    except Exception as e:
        print("Error validating code: {}".format(e))
        return False

def ForgotPasswordView(request):

    phone_verify = request.session.get('phone_verify', None)
    update_phone_verify = request.session.get('update_phone_verify', None)
    forgot_phone_verify = request.session.get('forgot_phone_verify', None)
    if phone_verify:
        del request.session['phone_verify']
    if update_phone_verify:
        del request.session['update_phone_verify']
    if forgot_phone_verify:
        del request.session['forgot_phone_verify']

    if request.method == 'POST' and not request.user.is_authenticated:
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            request.session['forgot_phone_verify'] = username
            userObj = User.objects.get(username=username)
            if userObj.usertype.is_student:
                code = send_verfication_code(to=userObj.usertype.userstudent.phone)
            else:
                code = send_verfication_code(to=userObj.usertype.userlandlord.phone)
            return redirect('user:verifyPhone')
        else:
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors.get(error), extra_tags='forgotPassword')
            # return JsonResponse(form.errors, status=400)

    return redirect('user:home')

def otpverify(request):
    context = {
        'forgotpass' : False,
        'blocked':  False,
        "form" : AuthenticationForm(),
        "LandlordSignupForm" : LandlordSignupForm(label_suffix=''),
        "StudentSignupForm"  : StudentSignupForm(label_suffix=''),
        "ForgotPasswordForm" : ForgotPasswordForm(label_suffix=''),
    }
    phone_verify = request.session.get('phone_verify', None)
    update_phone_verify = request.session.get('update_phone_verify', None)
    forgot_phone_verify = request.session.get('forgot_phone_verify', None)

    if phone_verify:
        userObj = get_object_or_404(User, username=phone_verify)
        phoneVerifyObj = PhoneVerification.objects.get_or_create(userObj=userObj)
        if not phoneVerifyObj[0].is_blocked:
            if phoneVerifyObj[1]:
                if userObj.usertype.is_student:
                    phoneVerifyObj[0].phone = userObj.usertype.userstudent.phone
                else:
                    phoneVerifyObj[0].phone = userObj.usertype.userlandlord.phone
                phoneVerifyObj[0].save()
                phoneVerifyObj[0].refresh_from_db()

            if request.method == "POST":
                form = VerificationCodeForm(request.POST)
                is_verified = False
                if form.is_valid():
                    is_verified = check_verification_code(phone=phoneVerifyObj[0].phone, code=form.cleaned_data.get('verificationCode'))
                if not is_verified:
                    if phoneVerifyObj[0].wrongAttemptCount > 1:
                        phoneVerifyObj[0].wrongAttemptCount -= 1
                        phoneVerifyObj[0].save()
                        messages.add_message(request, messages.WARNING, 'Wrong OTP')
                    else:
                        phoneVerifyObj[0].is_blocked = True
                        phoneVerifyObj[0].save()
                        context['blocked']= True
                        del request.session['phone_verify']
                else:
                    del request.session['phone_verify']
                    phoneVerifyObj[0].delete()
                    if userObj.usertype.is_student:
                        studentObj = get_object_or_404(UserStudent, user=userObj.usertype)
                        studentObj.phoneVerified = True
                        studentObj.save()
                    else:
                        landlordObj = get_object_or_404(UserLandLord, user=userObj.usertype)
                        landlordObj.phoneVerified = True
                        landlordObj.save()
                    # messages.add_message(request, messages.SUCCESS, 'Mobile verification completed. Sign in to you account.')
                    auth_login(request, userObj)
                    return redirect('user:home')

            context['PhoneNumberForm'] = PhoneNumberForm(initial={'verifyPhone':phoneVerifyObj[0].phone})
            context['VerificationForm'] = VerificationCodeForm()
            context['verifyUser']= phoneVerifyObj[0]
        else:
            context['blocked']= True
            del request.session['phone_verify']
        return render(request, 'users/verificationCode.html', context=context)

    if update_phone_verify and request.user.is_authenticated:
        phoneVerifyObj = PhoneVerification.objects.filter(userObj=request.user).first()
        if not phoneVerifyObj.is_blocked:
            if request.method == "POST":
                form = VerificationCodeForm(request.POST)
                is_verified = False
                if form.is_valid():
                    is_verified = check_verification_code(phone=phoneVerifyObj.phone, code=form.cleaned_data.get('verificationCode'))
                if not is_verified:
                    if phoneVerifyObj.wrongAttemptCount > 1:
                        phoneVerifyObj.wrongAttemptCount -= 1
                        phoneVerifyObj.save()
                        messages.add_message(request, messages.WARNING, 'Wrong OTP')
                    else:
                        phoneVerifyObj.is_blocked = True
                        phoneVerifyObj.save()
                        context['blocked']= True
                        del request.session['update_phone_verify']
                else:
                    del request.session['update_phone_verify']
                    messages.add_message(request, messages.SUCCESS, 'Mobile Number Updated Successfully.')
                    if request.user.usertype.is_student:
                        studentObj = get_object_or_404(UserStudent, user=request.user.usertype)
                        studentObj.phone = phoneVerifyObj.phone
                        studentObj.save()
                        phoneVerifyObj.delete()
                        return redirect('user:studentProfile', username=request.user.username)
                    else:
                        landlordObj = get_object_or_404(UserLandLord, user=request.user.usertype)
                        landlordObj.phone = phoneVerifyObj.phone
                        landlordObj.save()
                        phoneVerifyObj.delete()
                        return redirect('user:landlordProfile', username=request.user.username)

            context['VerificationForm'] = VerificationCodeForm()
            context['verifyUser']= phoneVerifyObj
            context['updateVerify']= True
        else:
            context['blocked']= True
            del request.session['update_phone_verify']
        return render(request, 'users/verificationCode.html', context=context)

    if forgot_phone_verify:
        userObj = get_object_or_404(User, username=forgot_phone_verify)
        phoneVerifyObj = PhoneVerification.objects.get_or_create(userObj=userObj)
        if userObj.usertype.is_student:
            userPhone = userObj.usertype.userstudent.phone
        else:
            userPhone = userObj.usertype.userlandlord.phone
        if phoneVerifyObj[1] or phoneVerifyObj[0].phone != userPhone:
            phoneVerifyObj[0].is_blocked = False
            phoneVerifyObj[0].phone = userPhone
            phoneVerifyObj[0].wrongAttemptCount = 3
            phoneVerifyObj[0].save()

        if not phoneVerifyObj[0].is_blocked:
            if request.method == "POST":
                form = VerificationCodeForm(request.POST)
                is_verified = False
                if form.is_valid():
                    is_verified = check_verification_code(phone=phoneVerifyObj[0].phone, code=form.cleaned_data.get('verificationCode'))
                if not is_verified:
                    if phoneVerifyObj[0].wrongAttemptCount > 1:
                        phoneVerifyObj[0].wrongAttemptCount -= 1
                        phoneVerifyObj[0].save()
                        messages.add_message(request, messages.WARNING, 'Wrong OTP')
                    else:
                        phoneVerifyObj[0].is_blocked = True
                        phoneVerifyObj[0].save()
                        context['blocked']= True
                        del request.session['forgot_phone_verify']
                else:
                    del request.session['forgot_phone_verify']
                    request.session['forgot_phone_verified'] = userObj.username
                    phoneVerifyObj[0].delete()
                    return redirect('user:setPass')
        else:
            context['blocked']= True
            del request.session['forgot_phone_verify']
        context['forgotpass']= True
        context['VerificationForm'] = VerificationCodeForm()
        context['verifyUser']= phoneVerifyObj[0]
        return render(request, 'users/verificationCode.html', context=context)

    return redirect('user:home')

def PhoneNumberUpdate(request):
    phone_verify = request.session.get('phone_verify', None)
    update_phone_verify = request.session.get('update_phone_verify', None)
    forgot_phone_verify = request.session.get('forgot_phone_verify', None)
    if request.method == "POST":
        if phone_verify:
            form = PhoneNumberForm(data=request.POST)
            if form.is_valid():
                userObj = get_object_or_404(User, username=phone_verify)
                phoneVeriObj = get_object_or_404(PhoneVerification, userObj=userObj)
                if userObj.usertype.is_student:
                    if userObj.usertype.userstudent.phone != form.cleaned_data.get('verifyPhone'):
                        userstudentObj = get_object_or_404(UserStudent, user=userObj.usertype)
                        userstudentObj.phone = form.cleaned_data.get('verifyPhone')
                        userstudentObj.save()
                        phoneVeriObj.phone = form.cleaned_data.get('verifyPhone')
                        phoneVeriObj.save()
                        phoneVeriObj.refresh_from_db()
                        code = send_verfication_code(to=phoneVeriObj.phone)
                else:
                    if userObj.usertype.userlandlord.phone != form.cleaned_data.get('verifyPhone'):
                        userlandlordObj = get_object_or_404(UserLandLord, user=userObj.usertype)
                        userlandlordObj.phone = form.cleaned_data.get('verifyPhone')
                        userlandlordObj.save()
                        phoneVeriObj.phone = form.cleaned_data.get('verifyPhone')
                        phoneVeriObj.save()
                        code = send_verfication_code(to=phoneVeriObj.phone)
            else:
                for error in form.errors:
                    messages.add_message(request, messages.ERROR, form.errors.get(error))
            return redirect('user:verifyPhone')
    if forgot_phone_verify:
        del self.request.session['forgot_phone_verify']
    return redirect('user:home')

def ResendVerificationCode(request, pk):
    phone_verify = request.session.get('phone_verify', None)
    update_phone_verify = request.session.get('update_phone_verify', None)
    forgot_phone_verify = request.session.get('forgot_phone_verify', None)

    if phone_verify:
        userObj = get_object_or_404(User, username=phone_verify)
        phoneverify = get_object_or_404(PhoneVerification, pk=pk)
        if userObj == phoneverify.userObj:
            if not phoneverify.is_blocked and phoneverify.resendCodeCount >= 1:
                code = send_verfication_code(to=phoneverify.phone)
                phoneverify.resendCodeCount -= 1
                phoneverify.save()
            return redirect('user:verifyPhone')

    if forgot_phone_verify:
        userObj = get_object_or_404(User, username=forgot_phone_verify)
        phoneverify = get_object_or_404(PhoneVerification, pk=pk)
        if userObj == phoneverify.userObj:
            if not phoneverify.is_blocked and phoneverify.resendCodeCount >= 1:
                code = send_verfication_code(to=phoneverify.phone)
                phoneverify.resendCodeCount -= 1
                phoneverify.save()
            return redirect('user:verifyPhone')

    if update_phone_verify and request.user.is_authenticated:
        phoneverify = get_object_or_404(PhoneVerification, pk=pk)
        if request.user == phoneverify.userObj:
            if not phoneverify.is_blocked and phoneverify.resendCodeCount >= 1:
                code = send_verfication_code(to=phoneverify.phone)
                phoneverify.resendCodeCount -= 1
                phoneverify.save()
            return redirect('user:verifyPhone')

    return redirect('user:home')

def ForgotSetPassword(request):
    forgot_phone_verified = request.session.get('forgot_phone_verified', None)

    if forgot_phone_verified:
        context = {
            "form" : AuthenticationForm(),
            "LandlordSignupForm" : LandlordSignupForm(label_suffix=''),
            "StudentSignupForm"  : StudentSignupForm(label_suffix=''),
            "ForgotPasswordForm" : ForgotPasswordForm(label_suffix=''),
        }
        userObj = get_object_or_404(User, username=forgot_phone_verified)
        form = ForgotSetPasswordForm(user=userObj)
        if request.method == "POST":
            form = ForgotSetPasswordForm(data=request.POST, user=userObj)
            if form.is_valid():
                form.save()
                del request.session['forgot_phone_verified']
                messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
                return redirect('user:home')

        context['passChangeForm'] = form
        return render(request, 'users/passwordChange.html', context=context)

    return redirect('user:home')

@login_required
@user_passes_test(studentAccessTest)
def StudentLivingHabitsUpdateView(request):
    if request.method == 'POST':
        student = get_object_or_404(UserStudent, user__user=request.user)
        form = StudentLivingHabitsForm(label_suffix='', data=request.POST, instance=student)
        if form.is_valid():
            form.instance.livingHabitsLater = True
            form.save()
    return redirect('students:roommates')
