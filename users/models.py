from django.db import models
import uuid

# Create your models here.
class USER(models.Model):
    user_id = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    email_id = models.EmailField()
    profile_picture = models.ImageField(blank=True,upload_to='images')
    college = models.TextField()


    def __str__(self):
        return self.email_id

    def __str__(self):
        return self.user_id

class LANDLORD(models.Model):
    l_id = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    email_id = models.EmailField()
    profile_picture = models.ImageField(blank=True,upload_to="images")

    def __str__(self):
        return self.l_id