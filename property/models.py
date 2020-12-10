from django.db import models
from django.contrib.gis.db import models as geoModel
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete, post_save
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.utils import timezone

import datetime, os

from users.models import UserLandLord, UserStudent
from .utils import unique_slug_generator, unique_file_path_generator, random_string_generator
from .locationApi import get_lat_long_from_address, get_near_by_text_places, get_near_by_types, logging
from .taskSchedulers import scheduler


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


class Property(geoModel.Model):
    
    landlord = models.ForeignKey(UserLandLord, on_delete=models.CASCADE)
    urlSlug = models.SlugField(unique=True, max_length=200, editable=False, verbose_name='URL')
    title = models.CharField(max_length=150, help_text="Title for your property")
    city = models.ForeignKey(CityList, on_delete=models.CASCADE, help_text="Select property located city")
    zipcode = models.CharField(max_length=5, verbose_name="Zip or Postal Code", validators=[
                        RegexValidator(regex=r'^\d{5}$', message='Only numbers allowed.'),
                        MinLengthValidator(5, '5 digit code'),
                    ], help_text="Eg 503 - 00503")
    address = models.CharField(max_length=250, help_text="Address of your property")
    location = geoModel.PointField(null=True, blank=True)
    locationType = models.CharField(null=True, blank=True, max_length=200)
    averageDistance = models.FloatField(default=0, help_text='Average distance between the nearby amenities (in miles).')
    placeId = models.CharField(null=True, blank=True, max_length=300)
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
    # utilities = models.BooleanField(default=False, help_text="Select if you have Utilities")
    garage = models.BooleanField(default=False, help_text="Select if you have Garage")
    parkingSpace = models.IntegerField(verbose_name="Parking Space", 
                            help_text="Available Parking Space. Eg 1 or 2",
                            validators=[
                                MinValueValidator(0, 'Minimum 0'),
                                MaxValueValidator(20, 'Maximum 20')
                            ],
                            default=0
                        )
    amenities = models.ManyToManyField(Amenities, help_text="Select 1 or more Amenities.")
    fromDate = models.DateField(verbose_name="From Date", 
                    help_text="From which date property available for rent"
                )
    toDate = models.DateField(verbose_name="To Date", 
                    help_text="Till which the property will be available."
                )
    likes = models.ManyToManyField(UserStudent, related_name="propLikes", blank=True)
    dislikes = models.ManyToManyField(UserStudent, related_name="propDislikes", blank=True)
    isleased = models.BooleanField(default=False)
    leaseStart = models.DateField(blank=True, null=True)
    leaseEnd = models.DateField(blank=True, null=True)
    updatedDate = models.DateTimeField(auto_now=True, verbose_name="Last Updated Date")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    class Meta:
        verbose_name_plural = "Properties"

    @property
    def totalLikes(self):
        return self.likes.count

    @property
    def totalDislikes(self):
        return self.dislikes.count

    def clean(self):
        errorMess = {}
        hasError = False
        if self.securityDeposit and self.amount == None:
            errorMess['amount'] = ValidationError(('Amount Field is required'), code='required')
            hasError = True

        if not self.securityDeposit:
            self.amount = None
        
        if self.fromDate is not None:
            if self.fromDate < datetime.date.today():
                alexists = Property.objects.filter(pk=self.pk).exists()
                if alexists:
                    check = Property.objects.get(pk=self.pk)
                    if check.fromDate != self.fromDate:
                        hasError = True
                        errorMess['fromDate'] = ValidationError(('From Date cannot be older than today.'), code='error')
                else:
                    hasError = True
                    errorMess['fromDate'] = ValidationError(('From Date cannot be older than today.'), code='error')

        if self.toDate is not None:
            if self.toDate <= self.fromDate:
                hasError = True
                errorMess['toDate'] = ValidationError(('To Date cannot be less than or equal to From Date.'), code='error')

        if self.address:
            try:
                fullAddress = '{}, {} {}'.format(self.address, self.city, self.zipcode)
                placeId, locationType, location, status = get_lat_long_from_address(fullAddress)
                # print(placeId, locationType, location, status)
                if status:
                    if placeId:
                        self.placeId = placeId
                    if locationType:
                        self.locationType = locationType
                    if location:
                        longitude = location.get('lng', 0)
                        latitude = location.get('lat', 0)
                        self.location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                else:
                    hasError = True
                    errorMess['address'] = ValidationError(('We are unable to locate the exact location. Please enter the address correctly.'), code='error')
            except Exception as e:
                print(e)

        if hasError:
            raise ValidationError(errorMess)


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


class PropertyNearby(geoModel.Model):
    
    propObject = models.ForeignKey(Property, on_delete=models.CASCADE)
    nearByType = models.CharField(max_length=100)
    nearByName = models.CharField(max_length=200, null=True, blank=True)
    location = geoModel.PointField(null=True, blank=True)
    placeId = models.CharField(max_length=300, null=True, blank=True)
    distanceToProp = models.FloatField(help_text='Distance to property in miles.', default=0)

    def __str__(self):
        return self.nearByType
    
    class Meta:
        ordering = ['distanceToProp']


class PropertyJobStore(models.Model):

    propObject = models.OneToOneField(Property, on_delete=models.CASCADE)
    jobid = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return address


class PostQuestion(models.Model):

    propKey = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="Property")
    student = models.ForeignKey(UserStudent, on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-createdDate']


class PostAnswer(models.Model):

    question = models.OneToOneField(PostQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer


# Signals and receivers of models here
@receiver(pre_save, sender=Property)
def auto_add_unique_slug_field(sender, instance, **kwargs):
    """
    Automatically add unique slug field to the Property models
    """
    instance.title = '{}, {} {}'.format(instance.address, instance.city, instance.zipcode)
    if instance.urlSlug:
        prop = Property.objects.get(pk=instance.pk)
        if instance.title != prop.title:
            instance.urlSlug = unique_slug_generator(instance)
    if not instance.urlSlug:
        instance.urlSlug = unique_slug_generator(instance)

def get_or_create_near_by(instance, nearByType):
    return PropertyNearby.objects.get_or_create(propObject=instance, nearByType=nearByType)

def fetch_near_by_places(instance):
    # {type_to_search: display name in frontend}
    nearByTypes = {'restaurant': 'Restaurant', 'shopping_mall': 'Shopping Mall', 'bar': 'Bar', }
    nearByText = {'Costco in': 'Costco', 'Target in': 'Target', 'Walmart in': 'Walmart', }
    for types in nearByTypes:
        success, nearPlaces = get_near_by_types(instance=instance, types=types)
        if success:
            for i, place in enumerate(nearPlaces):
                tempLoc = place.get('locationDict', None)
                longitude = tempLoc.get('lng', 0)
                latitude = tempLoc.get('lat', 0)
                location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                if i == 0:
                    obj = get_or_create_near_by(instance, nearByTypes[types])
                else:
                    obj = get_or_create_near_by(instance, '{}{}'.format(nearByTypes[types], i))
                obj[0].nearByName = place.get('nearByName', None)
                obj[0].location = location
                obj[0].placeId = place.get('placeId', None)
                obj[0].save()
    for place in nearByText:
        success, nearByName, locationDict, placeId = get_near_by_text_places(instance=instance, place=place)
        if success:
            longitude = locationDict.get('lng', 0)
            latitude = locationDict.get('lat', 0)
            location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
            obj = get_or_create_near_by(instance, nearByText[place])
            obj[0].nearByName = nearByName
            obj[0].location = location
            obj[0].placeId = placeId
            obj[0].save()
    nearbys = PropertyNearby.objects.filter(propObject=instance).annotate(distance=Distance(instance.location, 'location'))
    totalmiles = 0
    allplaces = nearByTypes
    allplaces.update(nearByText)
    allplaces = list(allplaces.values())
    count = len(allplaces)
    for nearby in nearbys:
        nearby.distanceToProp = nearby.distance.mi
        nearby.save()
        if nearby.nearByType in allplaces:
            totalmiles = totalmiles + nearby.distance.mi
    # if not instance.averageDistance or instance.averageDistance != round(totalmiles/count):
    instance.averageDistance = round(totalmiles/count, 1)
    instance.save()
    logging.info('Nearby location fetch finished for property "{}"'.format(instance.title))

def startFetchNearByJob(instance):
    jobId = random_string_generator(size=5)
    runDate = instance.updatedDate + datetime.timedelta(seconds=30)
    s = scheduler.add_job(fetch_near_by_places, 'date', [instance], run_date = runDate, id = jobId, misfire_grace_time=300, coalesce=True)
    logging.info('Nearby location fetch added for property "{}" and job id {}'.format(instance.title, jobId))
    return jobId

@receiver(post_save, sender=Property)
def auto_add_nearby_necessary_fields(sender, instance, **kwargs):
    """
    Automatically add near by necessary in the property.
    """
    address = '{}, {} {}'.format(instance.address, instance.city, instance.zipcode)
    if kwargs.get('created'):
        newJob = startFetchNearByJob(instance)
        PropertyJobStore.objects.create(propObject=instance, jobid=newJob, 
            address=address)
    else:
        if PropertyJobStore.objects.filter(propObject=instance).exists():
            oldJob = PropertyJobStore.objects.get(propObject=instance)
            if oldJob.address == address:
                oldJob_updated_time = oldJob.updatedDate + datetime.timedelta(days=30)
                if oldJob_updated_time <= timezone.now():
                    newJob = startFetchNearByJob(instance)
                    oldJob.address = address
                    oldJob.jobid = newJob
                    oldJob.save()
            else:
                newJob = startFetchNearByJob(instance)
                oldJob.address = address
                oldJob.jobid = newJob
                oldJob.save()
        else:
            newJob = startFetchNearByJob(instance)
            PropertyJobStore.objects.create(propObject=instance, jobid=newJob, 
                address=address)

# @receiver(pre_save, sender=PropertyImage)
# def auto_delete_property_image_on_modified(sender, instance, **kwargs):
#     """
#     Deletes Property image file from filesystem
#     when corresponding MediaFile object is modified.
#     """
#     if instance.imagePath:
#         alreadyExists = PropertyImage.objects.filter(pk=instance.pk).exists()
#         if alreadyExists:
#             oldFile = PropertyImage.objects.get(pk=instance.pk)
#             if str(oldFile.imagePath) != str(instance.imagePath):
#                 if os.path.isfile(oldFile.imagePath.path):
#                     os.remove(oldFile.imagePath.path)

# @receiver(post_delete, sender=PropertyImage)
# def auto_delete_property_image_on_delete(sender, instance, **kwargs):
#     """
#     Deletes Property image file from filesystem
#     when corresponding MediaFile object is deleted.
#     """
#     if instance.imagePath:
#         if os.path.isfile(instance.imagePath.path):
#             os.remove(instance.imagePath.path)

# @receiver(pre_save, sender=PropertyVideo)
# def auto_delete_property_video_on_modified(sender, instance, **kwargs):
#     """
#     Deletes Property video file from filesystem
#     when corresponding MediaFile object is modified.
#     """
#     if instance.videoPath:
#         alreadyExists = PropertyVideo.objects.filter(pk=instance.pk).exists()
#         if alreadyExists:
#             oldFile = PropertyVideo.objects.get(pk=instance.pk)
#             if str(oldFile.videoPath) != str(instance.videoPath):
#                 if os.path.isfile(oldFile.videoPath.path):
#                     os.remove(oldFile.videoPath.path)

# @receiver(post_delete, sender=PropertyVideo)
# def auto_delete_property_video_on_delete(sender, instance, **kwargs):
#     """
#     Deletes Property Video file from filesystem
#     when corresponding MediaFile object is deleted.
#     """
#     if instance.videoPath:
#         if os.path.isfile(instance.videoPath.path):
#             os.remove(instance.videoPath.path)

