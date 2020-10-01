from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

from .models import UserStudent, UserLandLord, UserType, Interest


class LandlordSignupForm(UserCreationForm):

    phone = PhoneNumberField()
    profilePicture = forms.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 
                    'password2', 'phone', 'profilePicture')


class StudentSignupForm(UserCreationForm):

    phone = PhoneNumberField()
    university = forms.CharField(max_length=50)
    classYear = forms.IntegerField()
    bio = forms.CharField(max_length=200)
    profilePicture = forms.ImageField()
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 
                    'password2', 'university', 'classYear', 'bio', 'interests', 'phone', 
                    'profilePicture')


# class SignUpForm(UserCreationForm):

#     regUserType = forms.ChoiceField(
#         widget=forms.RadioSelect(attrs={
#         }),
#         choices=[
#             ('student', "I'm a Student"), 
#             ('seller', "I'm a Seller")
#         ],
#         required=True,
#         label="",
#     )
#     is_college_student = forms.BooleanField(
#         widget=forms.CheckboxInput(attrs={
#             # 'onclick':"college_radio_click()",
#         }),
#         required=False,
#         label="Are you a college Student",
#     )
#     college_name = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': "Enter your college name",
#         }),
#         max_length=150, 
#         required=False,
#         label="College Name",
#     )
#     date_of_birth = forms.DateField(
#         widget=forms.DateInput(attrs={
#             'type':'date',
#             'class': 'form-control',
#         }),
#         label="Date of Birth",
#     )

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'regUserType', 'is_college_student', 
#                     'college_name', 'date_of_birth', 'password1', 'password2')
#         widgets = {
#             'first_name': forms.TextInput(attrs={
#                     'class': 'form-control',
#                     'placeholder': "Enter first name",
#                     'autofocus': True,
#                 }),
#             'last_name': forms.TextInput(attrs={
#                     'class': 'form-control',
#                     'placeholder': "Enter last name",
#                 }),
#             'email': forms.EmailInput(attrs={
#                     'class': 'form-control',
#                     'placeholder': "Enter your email address",
#                 }),
#         }
#         labels = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'email': 'Email'
#         }

#     def __init__(self, request=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['last_name'].required = True
#         self.fields['email'].required = True
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 
#             'placeholder': "Enter password",
#         })
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control',
#             'placeholder': "Re-Enter Password",
#         })
#         self.fields['password2'].label = "Confirm Password"

#     def clean(self):
#         if self.cleaned_data.get("email") and self.cleaned_data.get("regUserType"):
#             email = self.cleaned_data.get("email").lower()
#             regUserType = self.cleaned_data.get("regUserType")
#             isalreadyexists = False

#             try:
#                 UserType.objects.get(user__email=email, userType=regUserType)
#                 isalreadyexists = True
#             except UserType.DoesNotExist:
#                 isalreadyexists = False

#             if isalreadyexists:
#                 raise forms.ValidationError({'email': "Email already exists!"})


# class LoginInForm(forms.Form):

#     login_email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'autofocus': True,
#             'class': 'form-control',
#             'placeholder': "Enter your email address",
#         }),
#         required=True,
#         label="Email",
#     )
#     login_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': "Enter your password",
#         }),
#         strip=False,
#         required=True,
#         label="Password",
#     )
#     logUserType = forms.ChoiceField(
#         widget=forms.RadioSelect(attrs={
#         }),
#         choices=[
#             ('student', "I'm a Student"), 
#             ('seller', "I'm a Seller")
#         ],
#         required=True,
#         label="",
#     )


class StudentProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter first name",
        }),
        required=True,
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter last name",
        }),
        required=True,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your email address",
        }),
        required=True,
        label="Email",
    )

    class Meta:
        model = UserStudent
        fields = ('first_name', 'last_name', 'email', 'phone', 'university', 'classYear', 'bio', 
                    'interests', 'profilePicture')

        widgets = {
            'profilePicture': forms.ClearableFileInput(attrs={
                    'class': 'form-control',
                }),
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        studentInfo = get_object_or_404(UserStudent, pk=kwargs.get('instance').pk)
        self.fields['first_name'].initial = studentInfo.user.user.first_name
        self.fields['last_name'].initial = studentInfo.user.user.last_name
        self.fields['email'].initial = studentInfo.user.user.email


class LandlordProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter first name",
        }),
        required=True,
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter last name",
        }),
        required=True,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your email address",
        }),
        required=True,
    )

    class Meta:
        model = UserLandLord
        fields = ('first_name', 'last_name', 'email', 'phone', 'profilePicture')

        widgets = {
            'profilePicture': forms.ClearableFileInput(attrs={
                    'class': 'form-control',
                }),
            'phone': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'tel'
                }),
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        landlordInfo = get_object_or_404(UserLandLord, pk=kwargs.get('instance').pk)
        self.fields['first_name'].initial = landlordInfo.user.user.first_name
        self.fields['last_name'].initial = landlordInfo.user.user.last_name
        self.fields['email'].initial = landlordInfo.user.user.email