from django.db import models
# from django.contrib.auth.models import
from django.contrib.auth.models import User

# Create your models here.
class PROPERTY(models.Model):
    l_id = models.ForeignKey('users.LANDLORD',on_delete=models.CASCADE)
    property_id = models.CharField(max_length=40,primary_key=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    description = models.TextField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sqft = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.IntegerField()
    property_name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50)
    property_status = models.CharField(max_length=10)
    likes = models.ManyToManyField(User,related_name='properties')


class MEDIA(models.Model):
    media_path = models.TextField()
    media_type = models.CharField(max_length=10)
    p_id = models.ForeignKey(PROPERTY,on_delete=models.CASCADE)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    s_id = models.CharField(max_length=10)
