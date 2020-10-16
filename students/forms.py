from django import forms

from .models import RoommatePost

class RoommatePostForm(forms.ModelForm):
    
    class Meta:
        model = RoommatePost
        exclude = ['student', 'preference', 'heart']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title for your post',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share what you want...',
                'rows': '3'
            }),
            'interest': forms.CheckboxSelectMultiple(),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
