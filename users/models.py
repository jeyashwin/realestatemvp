from django.db import models

# Create your models here.
class USER(models.Model):
    user_id = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    email_id = models.EmailField()
    profile_picture = models.ImageField()
    college = models.TextField()

class LANDLORD(models.Model):
    user_id = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    email_id = models.EmailField()
    profile_picture = models.ImageField()