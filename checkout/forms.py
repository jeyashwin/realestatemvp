from django import forms

from .models import RequestToRentProperty


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
