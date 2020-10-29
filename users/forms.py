from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import UserStudent, UserLandLord, Interest, ContactUS
import phonenumbers

def validatePhone(number):
    try:
        phone = phonenumbers.parse(str(number), None)
        if phone.country_code != 1:
            # print(phone.country_code)
            # print(type(phone.country_code))
            raise ValidationError(_('Currently we accept only USA Numbers!'),)
    except phonenumbers.NumberParseException:
        pass

class LandlordSignupForm(UserCreationForm):

    phone = PhoneNumberField(
                widget=forms.TextInput(attrs={
                    'class': 'form-control formInput',
                    'type': 'tel',
                    'placeholder': 'Enter your phone number'
                }),
                help_text="Enter a valid USA phone number (e.g. (201) 555-0123)",
                validators=[validatePhone],
                region='US'
            )
    lanprofilePicture = forms.ImageField(
                            widget= forms.ClearableFileInput(attrs={
                                'class': 'form-control',
                                'style': 'display:none;',
                                'onchange': "landlordsignupprofilepicchanged(this)"
                            }),
                            label="Profile picture"
                        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 
                    'password2', 'phone', 'lanprofilePicture')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter first name",
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter last name",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter your email address",
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter username",
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control formInput', 
            'placeholder': "Enter password",
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control formInput',
            'placeholder': "Re-Enter Password",
        })
        self.fields['password2'].label = "Confirm Password"


class StudentSignupForm(UserCreationForm):

    usageChoices = [
        ('never', 'Never'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('occasionally', 'Occasionally')
    ]
    normalChoices = [
        ('daily', 'Daily'),
        ('occasionally', 'Occasionally'),
    ]

    phone = PhoneNumberField(
                widget=forms.TextInput(attrs={
                    'class': 'form-control formInput',
                    'type': 'tel',
                    'placeholder': 'Enter your phone number'
                }),
                help_text="Enter a valid USA phone number (e.g. (201) 555-0123)",
                validators=[validatePhone],
                region='US'
            )
    university = forms.CharField(max_length=50,
                    widget=forms.TextInput(attrs={
                        'class': 'form-control formInput',
                        'placeholder': 'Enter university name',
                    })
                )
    classYear = forms.IntegerField(validators=[
                        MinValueValidator(2010, "Minimum year 2010"), 
                        MaxValueValidator(2030, "Maximum year 2030")
                    ],
                    label='Class year',
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control formInput',
                        'placeholder': 'Enter class year'
                    })
                )
    bio = forms.CharField(max_length=200, 
            widget=forms.Textarea(attrs={
                'class': 'form-control formInput',
                'placeholder': 'Enter bio..',
                'rows': 2,
            })
        )
    profilePicture = forms.ImageField(
                        widget= forms.ClearableFileInput(attrs={
                            'class': 'form-control',
                            'style': 'display:none;',
                            'onchange': "studentsignupprofilepicchanged(this)",
                        }),
                        label="Profile picture"
                    )
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), 
                    widget=forms.CheckboxSelectMultiple()
                )
    fblink = forms.URLField(required=False, max_length=250, 
                widget=forms.URLInput(attrs={
                    'class': 'socialmediainput',
                    'placeholder': 'Enter facebook link',
                })
            )
    snapLink = forms.URLField(required=False, max_length=250,
                    widget=forms.URLInput(attrs={
                        'class': 'socialmediainput',
                        'placeholder': 'Enter snap chat link',
                    })
                )
    instaLink = forms.URLField(required=False, max_length=250, 
                    widget=forms.URLInput(attrs={
                        'class': 'socialmediainput',
                        'placeholder': 'Enter instagram link',
                    })
                )
    twitterLink = forms.URLField(required=False, max_length=250,
                    widget=forms.URLInput(attrs={
                        'class': 'socialmediainput',
                        'placeholder': 'Enter twitter link',
                    })
                )
    ssFrom = forms.TimeField(required=False, 
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                })
            )
    ssTo = forms.TimeField(required=False, 
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                })
            )
    shFrom = forms.TimeField(required=False, 
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                })
            )
    shTo = forms.TimeField(required=False, 
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                })
            )
    tbUsage = forms.ChoiceField(choices=usageChoices, required=False, 
                widget=forms.Select(attrs={
                    'class': 'form-control select2'
                })
            )
    alUsage = forms.ChoiceField(choices=usageChoices, required=False, 
                widget=forms.Select(attrs={
                    'class': 'form-control select2'
                })
            )
    cleanliness = forms.ChoiceField(choices=normalChoices, required=False, 
                widget=forms.Select(attrs={
                    'class': 'form-control select2'
                })
            )
    guests = forms.ChoiceField(choices=normalChoices, required=False, 
                widget=forms.Select(attrs={
                    'class': 'form-control select2'
                })
            )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 
                    'password2', 'university', 'classYear', 'bio', 'interests', 'phone', 
                    'profilePicture', 'fblink', 'snapLink', 'instaLink', 'twitterLink', 'ssFrom',
                    'ssTo', 'shFrom', 'shTo', 'tbUsage', 'alUsage', 'cleanliness', 'guests')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter first name",
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter last name",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter your email address",
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control formInput',
                'placeholder': "Enter username",
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control formInput', 
            'placeholder': "Enter password",
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control formInput',
            'placeholder': "Re-Enter Password",
        })
        self.fields['password2'].label = "Confirm Password"


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
                    'interests', 'profilePicture', 'fbLink', 'snapLink', 'instaLink', 'twitterLink', 
                    'sleepScheduleFrom', 'sleepScheduleTo', 'studyHourFrom', 'studyHourTo', 
                    'tobaccoUsage', 'alcoholUsage', 'cleanliness', 'guests')

        widgets = {
            'profilePicture': forms.ClearableFileInput(attrs={
                    'class': 'form-control',
                    'onchange': "loadPhoto(event)",
                }),
            'interests': forms.CheckboxSelectMultiple()
        }
        labels = {
            'fbLink': 'Facebook',
            'snapLink': 'SnapChat',
            'instaLink': 'Instagram', 
            'twitterLink': 'Twitter'
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
                    'onchange': "loadPhoto(event)",
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


class ContactUSForm(forms.ModelForm):

    class Meta:
        model = ContactUS
        fields = '__all__'

        widgets = {
            'contactEmail': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your queries here..',
                'rows': "4"
            }),
        }