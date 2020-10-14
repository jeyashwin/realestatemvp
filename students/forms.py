from django.forms import ModelForm

from .models import RoommatePost

class RoommatePostForm(ModelForm):
    
    class Meta:
        model = RoommatePost
        exclude = ['student', 'preference', 'heart']
