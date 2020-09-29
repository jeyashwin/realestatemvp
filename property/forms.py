from django import forms
from datetime import date

from .models import Property, PropertyImage, PropertyVideo, Amenities


class PropertyForm(forms.ModelForm):
    
    phoneNumber = forms.CharField(
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'disabled': True,
            'value': "21312312123"
        }),
        label = "Phone number",
        help_text="Your default Phone Number",
        required=False
    )

    class Meta:
        model = Property
        exclude = ['landlord', ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': "Enter property title",
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': "Describe the property...",
                'rows': '2'
            }),
            'city': forms.Select(attrs={
                'class': 'form-control custom-select',
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Zipcode",
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2'
            }),
            'parkingSpace': forms.NumberInput(attrs={
                'class': 'utiltiesExpand',
                'placeholder': '0'
            }),
            'rentPerPerson': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount'
            }),
            'occupants': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'sqft': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter deposit amount'
            }),
            'amenities': forms.CheckboxSelectMultiple(),
            'fromDate': forms.DateInput(attrs={
                'type':'date',
                'class': 'form-control',
                'min': date.today().strftime("%Y-%m-%d")
            }),
            'toDate': forms.DateInput(attrs={
                'type':'date',
                'class': 'form-control',
                'min': date.today().strftime("%Y-%m-%d")
            }),
        }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class PropertyImageForm(forms.ModelForm):
    
    class Meta:
        model = PropertyImage
        fields = ("imageDescription", "imagePath")
        widgets = {
            'imageDescription': forms.TextInput(attrs = {
                'class':'form-control imageDescriptionBox',
                'placeholder': 'Eg Bedroom Image'
            }),
            'imagePath':forms.ClearableFileInput(attrs = {'class':'form-control', 'style': 'display: none'}),
        }
        help_texts = {
            'imageDescription': "Minimum 4. Select the box to upload the image and describe that image in "
                                    "the below-given box."
        }


class PropertyVideoForm(forms.ModelForm):
    
    class Meta:
        model = PropertyVideo
        fields = ("videoDescription", "videoPath")
        widgets = {
            'videoDescription': forms.TextInput(attrs = {
                'class':'form-control videoDescriptionBox',
                'placeholder': 'Eg Bedroom Video'
            }),
            'videoPath':forms.ClearableFileInput(attrs = {
                'class': 'form-control', 
                'accept': 'video/*',
                'style': 'display: none'
            }),
        }
        help_texts = {
            'videoDescription': "Minimum 1. Select the box to upload the video and describe that video in "
                                    "the below-given box. Allowed extensions are: mov, mp4, avi, mkv"
        }


PropertyImageFormset = forms.inlineformset_factory(Property, PropertyImage, form=PropertyImageForm, 
                            extra=1, max_num=10, can_delete=True, min_num=4
                        )

PropertyVideoFormset = forms.inlineformset_factory(Property, PropertyVideo, form=PropertyVideoForm,
                            extra=1, max_num=4, can_delete=True, min_num=1
                        )


class PropertyFilterSortForm(forms.Form):

    choiceCommon = [
        ('1','1'), 
        ('2', '2'),
        ('3', '3'),
        ('>4', '4 or more'),
    ]

    sortChoices = [
        ('default', 'Default Sort'),
        ('p_low_hi', 'Price (Lo-Hi)'),
        ('p_hi_low', 'Price (Hi-Lo)'),
        ('room', 'Rooms'),
        ('bath', 'Baths'),
        ('sqft', 'SQFT')
    ]

    room = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=choiceCommon, 
                required=False)
    occp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=choiceCommon, 
                required=False)
    bath = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=choiceCommon, 
                required=False)
    minPri = forms.IntegerField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Min'}), min_value=1, required=False)
    maxPri = forms.IntegerField(widget=forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'Max'}), min_value=1, required=False)
    amenities = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), 
                queryset=Amenities.objects.all(), required=False)
    sort = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select'}), 
                choices=sortChoices, required=False)