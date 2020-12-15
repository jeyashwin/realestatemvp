from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

import uuid, os, random, string, phonenumbers

from .utils import unique_invite_code_generator

#User App model starts from here

def profile_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split('.')[-1]
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

    usageChoices = [
        ('never', 'Never'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('occasionally', 'Occasionally')
    ]
    normalChoices = [
        ('daily', 'Daily'),
        ('occasionally', 'Occasionally'),
    ]

    user = models.OneToOneField(UserType, on_delete=models.CASCADE)
    phone = PhoneNumberField(region='US')
    university = models.CharField(max_length=50)
    classYear = models.IntegerField(validators=[
                    MinValueValidator(2010, "Minimum year 2010"), 
                    MaxValueValidator(2030, "Maximum year 2030")
                ])
    bio = models.CharField(max_length=200)
    profilePicture = models.ImageField(upload_to=profile_image_file_path, default='uploads/avatar/profile_avatar.png')
    interests = models.ManyToManyField(Interest)
    fbLink = models.URLField(max_length=250, null=True, blank=True)
    snapLink = models.URLField(max_length=250, null=True, blank=True)
    instaLink = models.URLField(max_length=250, null=True, blank=True)
    twitterLink = models.URLField(max_length=250, null=True, blank=True)
    sleepScheduleFrom = models.TimeField(blank=True, null=True)
    sleepScheduleTo = models.TimeField(blank=True, null=True)
    studyHourFrom = models.TimeField(blank=True, null=True)
    studyHourTo = models.TimeField(blank=True, null=True)
    tobaccoUsage = models.CharField(max_length=100, choices=usageChoices, default='never')
    alcoholUsage = models.CharField(max_length=100, choices=usageChoices, default='never')
    cleanliness = models.CharField(max_length=100, choices=normalChoices, default='daily')
    guests = models.CharField(max_length=100, choices=normalChoices, default='daily')
    emailVerified = models.BooleanField(default=False)
    phoneVerified = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errorMess = {}
        if not self.user.is_student:
            errorMess['user'] = ValidationError(('User is not a student!'), code='invalid')
        
        if self.sleepScheduleFrom is not None and self.sleepScheduleTo is None:
            errorMess['sleepScheduleTo'] = ValidationError(('Sleep Schedule To Time is required!'), code='required')
        if self.sleepScheduleFrom is None and self.sleepScheduleTo is not None:
            errorMess['sleepScheduleFrom'] = ValidationError(('Sleep Schedule From Time is required!'), code='required')

        if self.studyHourFrom is not None and self.studyHourTo is None:
            errorMess['studyHourTo'] = ValidationError(('Study Hour To Time is required!'), code='required')
        if self.studyHourFrom is None and self.studyHourTo is not None:
            errorMess['studyHourFrom'] = ValidationError(('Study Hour From Time is required!'), code='required')
        
        # try:
        #     phone = phonenumbers.parse(str(self.phone), None)
        #     if phone.country_code != 1:
        #         # print(phone.country_code)
        #         # print(type(phone.country_code))
        #         errorMess['phone'] = ValidationError(('Currently we accept only USA Numbers!'), code='invalid phone')
        # except phonenumbers.NumberParseException:
        #     pass

        if errorMess is not None:
            raise ValidationError(errorMess)

    def __str__(self):
        return self.user.user.username


class UserLandLord(models.Model):
    """Custom userLandLord model that stores Seller information"""

    user = models.OneToOneField(UserType, on_delete=models.CASCADE)
    phone = PhoneNumberField(region='US')
    emailVerified = models.BooleanField(default=False)
    phoneVerified = models.BooleanField(default=False)
    profilePicture = models.ImageField(upload_to=profile_image_file_path, default='uploads/avatar/profile_avatar.png')
    createdDate = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errorMess = {}

        if not self.user.is_landlord:
            errorMess['user'] = ValidationError(('User is not a Seller!'), code='invalid')

        try:
            phone = phonenumbers.parse(str(self.phone), None)
            if phone.country_code != 1:
                # print(phone.country_code)
                # print(type(phone.country_code))
                errorMess['phone'] = ValidationError(('Currently we accept only USA Numbers!'), code='invalid phone')
        except phonenumbers.NumberParseException:
            pass

        if errorMess is not None:
            raise ValidationError(errorMess)

    def __str__(self):
        return self.user.user.username


class InviteCode(models.Model):
    """Stores student user invite code and the student who joined using that code."""

    student = models.OneToOneField(UserStudent, on_delete=models.CASCADE, related_name='student_invite')
    inviteCode = models.CharField(max_length=200, unique=True)
    studentJoined = models.ManyToManyField(UserStudent, related_name='joined_user', blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.inviteCode


class PhoneVerification(models.Model):
    """Stores user phone verification data"""

    userObj = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(region='US', blank=True, null=True)
    wrongAttemptCount = models.IntegerField(default=5)
    resendCodeCount = models.IntegerField(default=3)
    is_blocked = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.pk)


class ContactUS(models.Model):
    """Stores Contact US information"""

    contactEmail = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contactEmail

    class Meta:
        verbose_name_plural = 'Contact US'


# @receiver(models.signals.pre_save, sender=UserLandLord)
# def auto_delete_seller_profile_pic_on_modified(sender, instance, **kwargs):
#     """
#     Deletes Profile Picture file from filesystem
#     when corresponding MediaFile object is modified.
#     """
#     if instance.profilePicture:
#         alreadyExists = UserLandLord.objects.filter(pk=instance.pk).exists()
#         if alreadyExists:
#             oldFile = UserLandLord.objects.get(pk=instance.pk)
#             # +41524204242
#             if str(oldFile.profilePicture) != str(instance.profilePicture) and (str(oldFile.profilePicture) != ''):
#                 if os.path.isfile(oldFile.profilePicture.path):
#                     os.remove(oldFile.profilePicture.path)

# @receiver(models.signals.post_delete, sender=UserLandLord)
# def auto_delete_seller_profile_pic_on_delete(sender, instance, **kwargs):
#     """
#     Deletes Profile Picture file from filesystem
#     when corresponding MediaFile object is deleted.
#     """
#     if instance.profilePicture:
#         if os.path.isfile(instance.profilePicture.path):
#             os.remove(instance.profilePicture.path)

# @receiver(models.signals.pre_save, sender=UserStudent)
# def auto_delete_student_profile_pic_on_modified(sender, instance, **kwargs):
#     """
#     Deletes Profile Picture file from filesystem
#     when corresponding MediaFile object is modified.
#     """
#     if instance.profilePicture:
#         alreadyExists = UserStudent.objects.filter(pk=instance.pk).exists()
#         if alreadyExists:
#             oldFile = UserStudent.objects.get(pk=instance.pk)
#             if str(oldFile.profilePicture) != str(instance.profilePicture) and (str(oldFile.profilePicture) != ''):
#                 if os.path.isfile(oldFile.profilePicture.path):
#                     os.remove(oldFile.profilePicture.path)

@receiver(models.signals.post_save, sender=UserStudent)
def auto_create_invite_code_on_student_user_creation(sender, instance, **kwargs):
    """
    Auto create invite code on student user creation.
    """
    alreadyExists = InviteCode.objects.filter(student=instance).exists()
    if not alreadyExists:
        newInvite = InviteCode.objects.create(student=instance)
        newInvite.inviteCode = unique_invite_code_generator(instance=newInvite, size=20)
        newInvite.save()

# @receiver(models.signals.post_delete, sender=UserStudent)
# def auto_delete_student_profile_pic_on_delete(sender, instance, **kwargs):
#     """
#     Deletes Profile Picture file from filesystem
#     when corresponding MediaFile object is deleted.
#     """
#     if instance.profilePicture:
#         if os.path.isfile(instance.profilePicture.path):
#             os.remove(instance.profilePicture.path)
     