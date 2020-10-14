from django.db import models

from users.models import UserStudent
from property.models import Property
# Create your models here.

class Favourite(models.Model):

    student = models.OneToOneField(UserStudent, related_name="favourites", on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return "{}".format(self.pk)

