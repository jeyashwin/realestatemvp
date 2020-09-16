from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserBuyer, UserLandLord

class SignUpForm(UserCreationForm):

    regUserType = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
        }),
        choices=[
            ('buyer', "I'm a Buyer"), 
            ('seller', "I'm a Seller")
        ],
        required=True,
        label="",
    )
    is_college_student = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            # 'onclick':"college_radio_click()",
        }),
        required=False,
        label="Are you a college Student",
    )
    college_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your college name",
        }),
        max_length=150, 
        required=False,
        label="College Name",
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type':'date',
            'class': 'form-control',
            'placeholder': "Enter your college name",
        }),
        label="Date of Birth",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'regUserType', 'is_college_student', 
                    'college_name', 'date_of_birth', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "Enter first name",
                    'autofocus': True,
                }),
            'last_name': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "Enter last name",
                }),
            'email': forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': "Enter your email address",
                }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email'
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 
            'placeholder': "Enter password",
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control',
            'placeholder': "Re-Enter Password",
        })
        self.fields['password2'].label = "Confirm Password"

    def clean(self):
        email = self.cleaned_data["email"].lower()
        regUserType = self.cleaned_data["regUserType"]

        if regUserType == "buyer":
            try:
                UserBuyer.objects.get(user__email=email)
                isalreadyexits = True
            except UserBuyer.DoesNotExist:
                isalreadyexits = False

        elif  regUserType == "seller":
            try:
                UserLandLord.objects.get(user__email=email)
                isalreadyexits = True
            except UserLandLord.DoesNotExist:
                isalreadyexits = False
        
        if isalreadyexits:
            raise forms.ValidationError("Email already exists!")


class LoginInForm(forms.Form):

    login_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': "Enter your email address",
        }),
        required=True,
        label="Email",
    )
    login_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your password",
        }),
        strip=False,
        required=True,
        label="Password",
    )
    logUserType = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
        }),
        choices=[
            ('buyer', "I'm a Buyer"), 
            ('seller', "I'm a Seller")
        ],
        required=True,
        label="",
    )
