from django import forms

from .models import RequestToRentProperty, RequestToRentService


class RequestToRentPropertyForm(forms.ModelForm):

    class Meta:
        model = RequestToRentProperty
        fields = ['occupants', 'moveIn', 'moveOut']

        widgets = {
            'occupants': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width:100%; border-radius:50px;',
            }),
            'moveIn': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'border-radius:50px;',
                'type': 'date'
            }),
            'moveOut': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'border-radius:50px;',
                'type': 'date'
            })
        }


class RequestToRentServiceForm(forms.ModelForm):

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