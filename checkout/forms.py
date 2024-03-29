from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3

from .models import RequestToRentProperty, RequestToTourProperty, RequestToRentService


class RequestToRentPropertyForm(forms.ModelForm):
    rentcaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = RequestToRentProperty
        fields = ['occupants', 'moveIn', 'moveOut']

        widgets = {
            'occupants': forms.NumberInput(attrs={
                'class': 'form-control forminputrequests',
            }),
            'moveIn': forms.DateInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'date'
            }),
            'moveOut': forms.DateInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'date'
            })
        }


class RequestToTourPropertyForm(forms.ModelForm):

    tourcaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = RequestToTourProperty
        fields = ['preference1Date', 'preference1Time', 'preference2Date', 'preference2Time', 
                    'preference3Date', 'preference3Time']

        widgets = {
            'preference1Date': forms.DateInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'date'
            }),
            'preference1Time': forms.TimeInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'time'
            }),
            'preference2Date': forms.DateInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'date'
            }),
            'preference2Time': forms.TimeInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'time'
            }),
            'preference3Date': forms.DateInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'date'
            }),
            'preference3Time': forms.TimeInput(attrs={
                'class': 'form-control forminputrequests',
                'type': 'time'
            }),
        }


class RequestToRentServiceForm(forms.ModelForm):

    servicecaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = RequestToRentService
        exclude = ('serviceObj', 'studentObj', 'status')

        widgets = {
            'fromDate': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'width:100%; border-radius:50px;',
                'type': 'date'
            }),
            'toDate': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'width:100%; border-radius:50px;',
                'type': 'date'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter First name',
                'style' : 'width:100%; border-radius:50px;'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Last name',
                'style' : 'width:100%; border-radius:50px;'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'placeholder': 'Your Phone Number',
                'style': 'border-radius:50px;',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'style' : 'border-radius:50px;',
            }),
            'deliveryAddress': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Delivery Address',
                'style' : 'border-radius:30px;',
                'rows': '2',
            })
        }