from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

import uuid, os, random, string

#User App model starts from here

def profile_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profilePicture/', filename)


class UserBuyer(models.Model):
    """Custom userBuyer model that stores Buyer information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateField()
    isStudent = models.BooleanField(default=False)
    collegeName = models.CharField(max_length=150, blank=True)
    profilePicture = models.ImageField(upload_to=profile_image_file_path, blank=True)

    def __str__(self):
        return "{}".format(self.pk)

@receiver(models.signals.post_delete, sender=UserBuyer)
def auto_delete_seller_profile_pic_on_delete(sender, instance, **kwargs):
    """
    Deletes Profile Picture file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.profilePicture:
        if os.path.isfile(instance.profilePicture.path):
            os.remove(instance.profilePicture.path)


class UserLandLord(models.Model):
    """Custom userLandLord model that stores Seller information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateField()
    profilePicture = models.ImageField(upload_to=profile_image_file_path, blank=True)

    def __str__(self):
        return "{}".format(self.pk)

@receiver(models.signals.post_delete, sender=UserLandLord)
def auto_delete_buyer_profile_pic_on_delete(sender, instance, **kwargs):
    """
    Deletes Profile Picture file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.profilePicture:
        if os.path.isfile(instance.profilePicture.path):
            os.remove(instance.profilePicture.path)

def randomNumber():
    """Generate random number"""
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(4))

@receiver(models.signals.pre_save, sender=User)
def auto_add_unique_username_field(sender, instance, **kwargs):
    """
    Automatically add unique username field to the User models
    """
    if not instance.username:
        firstName_refactor = instance.first_name.strip().split(" ")
        username = "".join(firstName_refactor)
        
        while User.objects.filter(username=username):
            username = username + randomNumber()
        instance.username = username
    