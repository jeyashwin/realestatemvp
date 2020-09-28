from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

import datetime, os

from users.models import UserLandLord
from .utils import unique_slug_generator, unique_file_path_generator


# Create your models here.
class StateList(models.Model):

    stateFullName = models.CharField(max_length=150, 
                        help_text="Full name of State. Eg Newyork", 
                        verbose_name="State Name"
                    )
    stateShortName = models.CharField(max_length=10, 
                        help_text="Short name of a state. Eg Newyork - NY", 
                        verbose_name= "Short Form"
                    )

    def __str__(self):
        return self.stateFullName

class CityList(models.Model):

    state = models.ForeignKey(StateList, on_delete=models.CASCADE)
    cityName = models.CharField(max_length=150, help_text="City Name. Eg Stony Brook")

    def __str__(self):
        return '{}, {}'.format(self.cityName, self.state.stateShortName)


class Amenities(models.Model):

    amenityType = models.CharField(max_length=100, help_text="Type of Amenity. eg Pool, GYM etc",
                    verbose_name="Amenity Type")

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.amenityType


class Property(models.Model):
    
    landlord = models.ForeignKey(UserLandLord, on_delete=models.CASCADE)
    urlSlug = models.SlugField(unique=True, max_length=200, editable=False, verbose_name='URL')
    title = models.CharField(max_length=150, help_text="Title for your property")
    city = models.ForeignKey(CityList, on_delete=models.CASCADE, help_text="Select property located city")
    zipcode = models.CharField(max_length=5, verbose_name="Zip or Postal Code", validators=[
                        RegexValidator(regex=r'^\d{5}$', message='Only numbers allowed.'),
                        MinLengthValidator(5, '5 digit code'),
                    ], help_text="Eg 503 - 00503")
    address = models.CharField(max_length=250, help_text="Address of your property")
    sqft = models.FloatField(
                        verbose_name="Square Feet", 
                        help_text="Total Square feet of property",
                        validators=[MinValueValidator(1, "Square Feet should be atleast 1.")]
                    )
    occupants = models.IntegerField(help_text="Number of people can stay", validators=[
                        MinValueValidator(1, "Minimum 1"),
                        MaxValueValidator(20, "Maximum 20")
                    ])
    rooms = models.IntegerField(help_text="Available Rooms", validators=[
                        MinValueValidator(1, "Minimum 1"),
                        MaxValueValidator(20, "Maximum 20")
                    ])
    bathrooms= models.IntegerField(help_text="Number of Bathrooms", validators=[
                        MinValueValidator(1, "Minimum 1"),
                        MaxValueValidator(20, "Maximum 20")
                    ])
    securityDeposit = models.BooleanField(default=False, 
                            help_text="Select if security deposit needed",
                            verbose_name="Security Deposit"
                        )
    amount = models.IntegerField(null=True, blank=True, help_text="Security Deposit Amount in $", 
                            validators=[MinValueValidator(0, 'Minimum Amount cannot be lower than 0')]
                        )
    rentPerPerson = models.IntegerField(verbose_name="Rent Per Person", help_text="Amount in $", 
                            validators=[MinValueValidator(0, 'Minimum Price cannot be lower than 0')]
                        )
    description = models.TextField(help_text="Describe about your property", max_length=500)
    utilities = models.BooleanField(default=False, help_text="Select if you have Utilities")
    garage = models.BooleanField(default=False, help_text="Select if you have Garage")
    parkingSpace = models.IntegerField(blank=True, null=True, verbose_name="Parking Space", 
                            help_text="Available Parking Space. Eg 1 or 2",
                            validators=[
                                MinValueValidator(0, 'Minimum 0'),
                                MaxValueValidator(20, 'Maximum 20')
                            ]
                        )
    amenities = models.ManyToManyField(Amenities, help_text="Select 1 or more Amenities.")
    fromDate = models.DateField(verbose_name="From Date", 
                    help_text="From which date property available for rent"
                )
    toDate = models.DateField(verbose_name="To Date", 
                    help_text="Till which the property will be available."
                )
    updatedDate = models.DateTimeField(auto_now=True, verbose_name="Last Updated Date")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    # lat = models.DecimalField(max_digits=9, decimal_places=6)
    # lon = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        verbose_name_plural = "Properties"

    def clean(self):
        if self.securityDeposit and self.amount == None:
            raise ValidationError({'amount': ValidationError(('Amount Field is required'), code='required')})

        if not self.securityDeposit:
            self.amount = None
        
        if self.fromDate < datetime.date.today():
            alexists = Property.objects.filter(pk=self.pk).exists
            if alexists:
                check = Property.objects.get(pk=self.pk)
                if check.fromDate != self.fromDate:
                    raise ValidationError({'fromDate': ValidationError(('From Date cannot be older than today.'), code='error')})
            else:
                raise ValidationError({'fromDate': ValidationError(('From Date cannot be older than today.'), code='error')})

        if self.toDate <= self.fromDate:
            raise ValidationError({'toDate': ValidationError(('To Date cannot be less than or equal to From Date.'), code='error')})

    def __str__(self):
        return "{} {}".format(self.pk, self.title)


class PropertyImage(models.Model):
    
    propertyKey = models.ForeignKey(Property, on_delete=models.CASCADE)
    imageDescription = models.CharField(max_length=50, verbose_name="Image Description", 
                            help_text="Describe about image. Eg Bathroom"
                        )
    imagePath = models.ImageField(upload_to=unique_file_path_generator, verbose_name="Image")

    @property
    def mediaType(self):
        return 'propimage'

    def __str__(self):
        return "{}".format(self.pk)


class PropertyVideo(models.Model):

    propertyKey = models.ForeignKey(Property, on_delete=models.CASCADE)
    videoDescription = models.CharField(max_length=50, verbose_name="Video Description", 
                            help_text="Describe about video. Eg Bedroom 1"
                        )
    videoPath = models.FileField(upload_to=unique_file_path_generator, verbose_name="Video", 
                            help_text= "Allowed extentions are: mov, mp4, avi, mkv"
                        )

    @property
    def mediaType(self):
        return 'propvideo'

    def clean(self):
        videoPath = str(self.videoPath)
        if 'uploads/property/' not in videoPath:
            allowedExtension = ['mov', 'mp4', 'avi', 'mkv']
            extension = videoPath.split('.')[-1]
            if extension not in allowedExtension:
                errorMessage = "File extension '{}' is not allowed. Allowed extensions are: {}.".format(
                                extension, str(allowedExtension))
                raise ValidationError({'videoPath': ValidationError((errorMessage), code='error')})

    def __str__(self):
        return "{}".format(self.pk)


# Signals and receivers of models here
@receiver(pre_save, sender=Property)
def auto_add_unique_slug_field(sender, instance, **kwargs):
    """
    Automatically add unique slug field to the Property models
    """
    if instance.urlSlug:
        prop = Property.objects.get(pk=instance.pk)
        if instance.title != prop.title:
            instance.urlSlug = unique_slug_generator(instance)
    if not instance.urlSlug:
        instance.urlSlug = unique_slug_generator(instance)

@receiver(pre_save, sender=PropertyImage)
def auto_delete_property_image_on_modified(sender, instance, **kwargs):
    """
    Deletes Property image file from filesystem
    when corresponding MediaFile object is modified.
    """
    if instance.imagePath:
        alreadyExists = PropertyImage.objects.filter(pk=instance.pk).exists()
        if alreadyExists:
            oldFile = PropertyImage.objects.get(pk=instance.pk)
            if str(oldFile.imagePath) != str(instance.imagePath):
                if os.path.isfile(oldFile.imagePath.path):
                    os.remove(oldFile.imagePath.path)

@receiver(post_delete, sender=PropertyImage)
def auto_delete_property_image_on_delete(sender, instance, **kwargs):
    """
    Deletes Property image file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.imagePath:
        if os.path.isfile(instance.imagePath.path):
            os.remove(instance.imagePath.path)

@receiver(pre_save, sender=PropertyVideo)
def auto_delete_property_video_on_modified(sender, instance, **kwargs):
    """
    Deletes Property video file from filesystem
    when corresponding MediaFile object is modified.
    """
    if instance.videoPath:
        alreadyExists = PropertyVideo.objects.filter(pk=instance.pk).exists()
        if alreadyExists:
            oldFile = PropertyVideo.objects.get(pk=instance.pk)
            if str(oldFile.videoPath) != str(instance.videoPath):
                if os.path.isfile(oldFile.videoPath.path):
                    os.remove(oldFile.videoPath.path)

@receiver(post_delete, sender=PropertyVideo)
def auto_delete_property_video_on_delete(sender, instance, **kwargs):
    """
    Deletes Property Video file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.videoPath:
        if os.path.isfile(instance.videoPath.path):
            os.remove(instance.videoPath.path)

