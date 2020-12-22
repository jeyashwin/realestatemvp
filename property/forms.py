from django import forms
from django.db.models import Max, Min
from datetime import date
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.auth import settings
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from .models import Property, PropertyImage, PropertyVideo, Amenities

longitude = -73.12082590786636
latitude = 40.91638132127517
userlocation = Point(longitude, latitude, srid=4326)

class PropertyForm(forms.ModelForm):

    amenity1 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Pool'
        }),
        # help_text="Add Minimum 4 Amenities.",
        required=False,
    )
    amenity2 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Gym'
        }),
        required=False,
    )
    amenity3 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Furnished'
        }),
        required=False,
    )
    amenity4 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Unfurnished'
        }),
        required=False,
    )
    amenity5 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Wifi'
        }),
        required=False,
    )
    amenity6 = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex Air Condition'
        }),
        required=False,
    )

    propertycaptcha = ReCaptchaField(
            public_key=settings.RECAPTCHA_V3_PUBLIC_KEY,
            private_key=settings.RECAPTCHA_V3_PRIVATE_KEY,
            widget=ReCaptchaV3()
        )
    
    class Meta:
        model = Property
        exclude = ['title', 'landlord', 'likes', 'dislikes', 'amenities', 'averageDistance', 'location',
                    'locationType', 'placeId', 'isleased', 'leaseStart', 'leaseEnd', ]

        widgets = {
            # 'title': forms.TextInput(attrs={
            #     'class': 'form-control', 
            #     'placeholder': "Enter property title",
            # }),
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
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex 1380, stonybrook'
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
            # 'amenities': forms.CheckboxSelectMultiple(),
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
        if self.initial:
            for count, i in enumerate(self.instance.amenities.all()):
                if count < 7:
                    self.fields['amenity{}'.format(count+1)].initial = i.amenityType
            self.fields['fromDate'].widget = forms.DateInput(attrs={
                'type':'date',
                'class': 'form-control',
                'min': self.instance.fromDate
            })
            self.fields['toDate'].widget = forms.DateInput(attrs={
                'type':'date',
                'class': 'form-control',
                'min': self.instance.toDate
            })


class PropertyImageForm(forms.ModelForm):
    
    class Meta:
        model = PropertyImage
        fields = ("imageDescription", "imagePath")
        widgets = {
            'imageDescription': forms.TextInput(attrs = {
                'class':'form-control imageDescriptionBox',
                'placeholder': 'Ex Bedroom Image'
            }),
            'imagePath':forms.ClearableFileInput(attrs = {'class':'form-control', 'style': 'display: none'}),
        }
        help_texts = {
            'imageDescription': "Minimum 3. Select the box to upload the image and describe that image in "
                                    "the below-given box."
        }


class PropertyVideoForm(forms.ModelForm):
    
    class Meta:
        model = PropertyVideo
        fields = ("videoDescription", "videoPath")
        widgets = {
            'videoDescription': forms.TextInput(attrs = {
                'class':'form-control videoDescriptionBox',
                'placeholder': 'Ex Bedroom Video'
            }),
            'videoPath':forms.ClearableFileInput(attrs = {
                'class': 'form-control', 
                'accept': 'video/*',
                'style': 'display: none'
            }),
        }
        help_texts = {
            'videoDescription': "Select the box to upload the video and describe that video in "
                                    "the below-given box. Allowed extensions are: mov, mp4, avi, mkv"
        }


PropertyImageFormset = forms.inlineformset_factory(Property, PropertyImage, form=PropertyImageForm, 
                            extra=1, max_num=10, can_delete=True, min_num=2
                        )

PropertyVideoFormset = forms.inlineformset_factory(Property, PropertyVideo, form=PropertyVideoForm,
                            extra=1, max_num=4, can_delete=True
                        )


class PropertyFilterSortForm(forms.Form):

    sortChoices = [
        ('default', 'Default Sort'),
        ('p_low_hi', 'Price (Lo-Hi)'),
        ('p_hi_low', 'Price (Hi-Lo)'),
        ('room', 'Rooms'),
        ('bath', 'Baths'),
        # ('sqft', 'SQFT')
    ]
    commonChoices = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '+4')
    ]
    room = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=commonChoices, required=False)
    occp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=commonChoices, required=False)
    bath = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=commonChoices, required=False)
    minPri = forms.IntegerField(required=False)
    maxPri = forms.IntegerField(required=False)
    disPro = forms.FloatField(required=False)
    disAmen = forms.FloatField(required=False)
    # amenities = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
    #                 'style': 'display:none; margin-top:10px;'
    #             }), 
    #             queryset=Amenities.objects.all(), required=False)
    sort = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select'}), 
                choices=sortChoices, required=False)

    def __init__(self, request=None, *args, **kwargs):
        super(PropertyFilterSortForm, self).__init__(*args, **kwargs)
        obj = Property.objects.all().annotate(distance=Distance(userlocation, 'location'))
        maxp = obj.aggregate(Max('rentPerPerson'))
        minp = obj.aggregate(Min('rentPerPerson'))
        maxDisP = obj.aggregate(Max('distance'))
        minDisP = obj.aggregate(Min('distance'))
        minDistanceInMile = minDisP.get('distance__min', 0)
        maxDistanceInMile = maxDisP.get('distance__max', 0)
        if type(minDistanceInMile) != type(0):
            if minDistanceInMile:
                minDistanceInMile = round(minDistanceInMile.mi, 1)
        if type(maxDistanceInMile) != type(0):
            if maxDistanceInMile:
                maxDistanceInMile = round(maxDistanceInMile.mi, 1)
        maxDisA = obj.aggregate(Max('averageDistance'))
        minDisA = obj.aggregate(Min('averageDistance'))
        self.fields['minPri'] = forms.IntegerField(
                                    widget=forms.NumberInput(attrs={
                                        'placeholder': 'Min', 'type': 'range', 'step': '1',
                                        'value': minp.get('rentPerPerson__min', 0)
                                    }),
                                    min_value=minp.get('rentPerPerson__min', 0),
                                    max_value=maxp.get('rentPerPerson__max', 0),
                                    required=False
                                )
        self.fields['maxPri'] = forms.IntegerField(
                                    widget=forms.NumberInput(attrs={
                                        'placeholder': 'Max', 'type': 'range', 'step': '1',
                                        'value': maxp.get('rentPerPerson__max', 0)
                                    }),
                                    max_value = maxp.get('rentPerPerson__max', 0),
                                    min_value = minp.get('rentPerPerson__min', 0),
                                    required=False,
                                )
        self.fields['disPro'] = forms.FloatField(
                                    widget=forms.NumberInput(attrs={
                                        'placeholder': 'Property Distance', 
                                        'type': 'range', 'step': '0.1',
                                        'value': maxDistanceInMile
                                    }),
                                    min_value=minDistanceInMile,
                                    max_value=maxDistanceInMile,
                                    required=False
                                )
        self.fields['disAmen'] = forms.FloatField(
                                    widget=forms.NumberInput(attrs={
                                        'placeholder': 'Property Amenity', 
                                        'type': 'range', 'step': '0.1',
                                        'value': maxDisA.get('averageDistance__max', 0)
                                    }),
                                    min_value=minDisA.get('averageDistance__min', 0),
                                    max_value=maxDisA.get('averageDistance__max', 0),
                                    required=False
                                )
    
    def clean(self):
        minprice = self.cleaned_data.get("minPri")
        maxprice = self.cleaned_data.get("maxPri")
        if minprice and maxprice:
            if minprice >= maxprice:
                raise forms.ValidationError({'minPri': "minimum price must be less than max price"})
