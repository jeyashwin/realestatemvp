from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UsernameField, SetPasswordForm
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import settings
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3

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
    
    landlordcaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 
                    'password2', 'phone', 'lanprofilePicture', 'landlordcaptcha')
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

    def clean(self):
        uniqueUserName = self.cleaned_data.get('username', None)
        if uniqueUserName:
            self.cleaned_data['username'] = uniqueUserName.lower()
        return super().clean()


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
    # interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), 
    #                 widget=forms.CheckboxSelectMultiple()
    #             )
    interest1 = forms.CharField(max_length=100,
                    widget=forms.TextInput(attrs={
                        'class': 'interestTextbox',
                        'placeholder': 'Ex Adventuring'
                    }),
                )
    interest2 = forms.CharField(max_length=100,
                    widget=forms.TextInput(attrs={
                        'class': 'interestTextbox',
                        'placeholder': 'Ex Cycling'
                    }),
                )
    interest3 = forms.CharField(max_length=100,
                    widget=forms.TextInput(attrs={
                        'class': 'interestTextbox',
                        'placeholder': 'Ex Partying'
                    }),
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
    ssFrom = forms.TimeField( 
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                }),
            )
    ssTo = forms.TimeField(
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                })
            )
    shFrom = forms.TimeField(
                widget=forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type': 'time'
                })
            )
    shTo = forms.TimeField(
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
    
    studentcaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 
                    'password2', 'university', 'classYear', 'bio', 'interest1', 'interest2', 
                    'interest3', 'phone', 'profilePicture', 'fblink', 'snapLink', 'instaLink', 
                    'twitterLink', 'ssFrom', 'ssTo', 'shFrom', 'shTo', 'tbUsage', 'alUsage', 
                    'cleanliness', 'guests', 'studentcaptcha')
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

    def clean(self):
        errorMess = {}

        uniqueUserName = self.cleaned_data.get('username', None)
        if uniqueUserName:
            self.cleaned_data['username'] = uniqueUserName.lower()

        if self.cleaned_data.get('ssFrom') is not None and self.cleaned_data.get('ssTo') is None:
            errorMess['ssTo'] = ValidationError(_('Sleep Schedule To Time is required!'), code='required')
        if self.cleaned_data.get('ssFrom') is None and self.cleaned_data.get('ssTo') is not None:
            errorMess['ssFrom'] = ValidationError(_('Sleep Schedule From Time is required!'), code='required')

        if self.cleaned_data.get('shFrom') is not None and self.cleaned_data.get('shTo') is None:
            errorMess['shTo'] = ValidationError(_('Study Hour To Time is required!'), code='required')
        if self.cleaned_data.get('shFrom') is None and self.cleaned_data.get('shTo') is not None:
            errorMess['shFrom'] = ValidationError(_('Study Hour From Time is required!'), code='required')

        if errorMess != {}:
            raise ValidationError(errorMess)
        return super().clean()


class StudentProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter first name",
        }),
        required=True,
        label='First Name',
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter last name",
        }),
        required=True,
        label='Last Name',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your email address",
        }),
        required=True,
    )
    interest1 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Adventuring'
        }),
    )
    interest2 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Cycling'
        }),
    )
    interest3 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Partying'
        }),
    )
    Updatephone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'tel',
            'placeholder': 'Enter your phone number'
        }),
        help_text="Enter a valid USA phone number (e.g. (201) 555-0123)",
        # validators=[validatePhone],
        region='US',
        label='Phone'
    )
    studentProfilecaptcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_V3_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_V3_PRIVATE_KEY,
        widget=ReCaptchaV3()
    )

    class Meta:
        model = UserStudent
        fields = ('first_name', 'last_name', 'email', 'Updatephone', 'university', 'classYear', 'bio', 
                    'interest1', 'interest2', 'interest3', 'profilePicture', 'fbLink', 
                    'instaLink', 'twitterLink', 'sleepScheduleFrom', 'sleepScheduleTo', 
                    'studyHourFrom', 'studyHourTo', 'tobaccoUsage', 'alcoholUsage', 'cleanliness',
                    'guests', 'studentProfilecaptcha')

        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bio..',
                'rows': 2,
            }),
            'profilePicture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'onchange': "loadPhoto(event)",
            }),
            'tobaccoUsage': forms.Select(attrs={
                'class': 'form-control',
            }),
            'alcoholUsage': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cleanliness': forms.Select(attrs={
                'class': 'form-control',
            }),
            'guests': forms.Select(attrs={
                'class': 'form-control',
            }),
            'sleepScheduleFrom': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }, format='%H:%M'), 
            'sleepScheduleTo':  forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }, format='%H:%M'),
            'studyHourFrom':  forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }, format='%H:%M'),
            'studyHourTo':  forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }, format='%H:%M'),
        }
        labels = {
            'classYear': 'Class Year',
            'fbLink': 'Facebook',
            'instaLink': 'Instagram', 
            'twitterLink': 'Twitter',
            'sleepScheduleFrom': 'Sleep Schedule From', 
            'sleepScheduleTo': 'Sleep Schedule To', 
            'studyHourFrom': 'Study Hour From', 
            'studyHourTo': 'Study Hour To', 
            'tobaccoUsage': 'Tobacco Usage',
            'alcoholUsage': 'Alcohol Usage',
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        studentInfo = get_object_or_404(UserStudent, pk=kwargs.get('instance').pk)
        for count, i in enumerate(studentInfo.interests.all()):
            if count < 3:
                self.fields['interest{}'.format(count+1)].initial = i.interest
        self.fields['first_name'].initial = studentInfo.user.user.first_name
        self.fields['last_name'].initial = studentInfo.user.user.last_name
        self.fields['email'].initial = studentInfo.user.user.email
        self.fields['Updatephone'].initial = studentInfo.phone

        self.label_suffix = ''


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
    Updatephone = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'tel',
            'placeholder': 'Enter your phone number'
        }),
        help_text="Enter a valid USA phone number (e.g. (201) 555-0123)",
        validators=[validatePhone],
        region='US',
        label='Phone'
    )
    landlordProfilecaptcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_V3_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_V3_PRIVATE_KEY,
        widget=ReCaptchaV3()
    )

    class Meta:
        model = UserLandLord
        fields = ('first_name', 'last_name', 'email', 'Updatephone', 'profilePicture', 'landlordProfilecaptcha')

        widgets = {
            'profilePicture': forms.ClearableFileInput(attrs={
                    'class': 'form-control',
                    'onchange': "loadPhoto(event)",
                }),
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        landlordInfo = get_object_or_404(UserLandLord, pk=kwargs.get('instance').pk)
        self.fields['first_name'].initial = landlordInfo.user.user.first_name
        self.fields['last_name'].initial = landlordInfo.user.user.last_name
        self.fields['email'].initial = landlordInfo.user.user.email
        self.fields['Updatephone'].initial = landlordInfo.phone


class ContactUSForm(forms.ModelForm):

    captchaVerification = ReCaptchaField(widget=ReCaptchaV2Checkbox())

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
                'placeholder': 'Enter your messages here..',
                'rows': "4"
            }),
        }

class ForgotPasswordForm(forms.Form):

    error_messages = {
        'username_not_exists': _('The username not exists'),
        'phone_not_verified': _("The account doesn't has verified phone" ),
        'unknown_error': _("Unable to Proceed.")
    }
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    forgotcaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    def clean(self):
        username = self.cleaned_data.get('username').lower()
        if not User.objects.filter(username=username).exists():
            raise ValidationError(
                self.error_messages['username_not_exists'],
                code='username_not_exists',
            )
        else:
            user = User.objects.get(username=username)
            if not user.is_superuser and not user.is_staff:
                if user.usertype.is_student:
                    if not user.usertype.userstudent.phoneVerified:
                        raise ValidationError(
                            self.error_messages['phone_not_verified'],
                            code='phone_not_verified',
                        )
                else:
                    if not user.usertype.userlandlord.phoneVerified:
                        raise ValidationError(
                            self.error_messages['phone_not_verified'],
                            code='phone_not_verified',
                        )
            else:
                raise ValidationError(
                    self.error_messages['unknown_error'],
                    code='unknown_error',
                )


class PhoneNumberForm(forms.Form):

    changePhonecaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    verifyPhone = PhoneNumberField(
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'tel',
                    'placeholder': 'Enter your phone number'
                }),
                help_text="Enter a valid USA phone number (e.g. (201) 555-0123)",
                # validators=[validatePhone],
                region='US'
            )

class VerificationCodeForm(forms.Form):

    verificationCode = forms.CharField(
        widget=forms.TextInput(attrs={
                'class': 'form-control text-center',
                'placeholder': '__ __ __ __ __ __',
                'maxlength': '6',
            }
        ),
        validators=[
            RegexValidator(regex=r'^\d{6}$', message='Only numbers allowed.'),
            MinLengthValidator(6, '6 digit code'),
        ]
    )

class ForgotSetPasswordForm(SetPasswordForm):
    
    setPasscaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())