from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

import uuid, os, random, string

#User App model starts from here

def profile_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split('.')[-1]
    print(ext)
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profilePicture/', filename)

class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userType = models.CharField(max_length=50, choices=[('student', 'Student'), ('seller', 'Seller')])
    student = models.BooleanField(default=False, editable=False)
    landLord = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.userType == "student":
            self.student = True
            self.landLord = False
        else:
            self.landLord = True
            self.student = False
        return super().save(*args, **kwargs)

    @property
    def is_student(self):
        return self.student
    
    @property
    def is_landlord(self):
        return self.landLord

    def __str__(self):
        return self.user.username


class Interest(models.Model):

    interest = models.CharField(max_length=100, help_text="Type of Interest. eg Partying, Sports etc")

    def __str__(self):
        return self.interest


class UserStudent(models.Model):
    """Custom userStudent model that stores Student information"""

    user = models.OneToOneField(UserType, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    university = models.CharField(max_length=50)
    classYear = models.IntegerField()
    bio = models.CharField(max_length=200)
    profilePicture = models.ImageField(upload_to=profile_image_file_path)
    interests = models.ManyToManyField(Interest)
    emailVerified = models.BooleanField(default=False)
    phoneVerified = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.user.is_student:
            raise ValidationError({'user': ValidationError(('User is not a student!'), code='invalid')})

    def __str__(self):
        return self.user.user.username


class UserLandLord(models.Model):
    """Custom userLandLord model that stores Seller information"""

    user = models.OneToOneField(UserType, on_delete=models.CASCADE)
    phone = PhoneNumberField()
    emailVerified = models.BooleanField(default=False)
    phoneVerified = models.BooleanField(default=False)
    profilePicture = models.ImageField(upload_to=profile_image_file_path)
    createdDate = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.user.is_landlord:
            raise ValidationError({'user': ValidationError(('User is not a Seller!'), code='invalid')})

    def __str__(self):
        return self.user.user.username


@receiver(models.signals.post_delete, sender=UserLandLord)
def auto_delete_seller_profile_pic_on_delete(sender, instance, **kwargs):
    """
    Deletes Profile Picture file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.profilePicture:
        if os.path.isfile(instance.profilePicture.path):
            os.remove(instance.profilePicture.path)

@receiver(models.signals.post_delete, sender=UserStudent)
def auto_delete_student_profile_pic_on_delete(sender, instance, **kwargs):
    """
    Deletes Profile Picture file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.profilePicture:
        if os.path.isfile(instance.profilePicture.path):
            os.remove(instance.profilePicture.path)

# def randomNumber():
#     """Generate random number"""
#     numbers = string.digits
#     return ''.join(random.choice(numbers) for i in range(4))

# @receiver(models.signals.pre_save, sender=User)
# def auto_add_unique_username_field(sender, instance, **kwargs):
#     """
#     Automatically add unique username field to the User models
#     """
#     if not instance.username:
#         firstName_refactor = instance.first_name.strip().split(" ")
#         username = "".join(firstName_refactor)
        
#         while User.objects.filter(username=username):
#             username = username + randomNumber()
#         instance.username = username
    