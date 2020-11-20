from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

import uuid, os

# from users.models import UserStudent, Interest
from users.models import UserStudent
from property.models import Property
# from .utils import unique_slug_generator_preference, random_string_generator

# Create your models here.

def roompost_image_file_path(instance, filename):
    """Generate file path for new roompost image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/post/', filename)


class Favourite(models.Model):

    student = models.OneToOneField(UserStudent, related_name="favourites", on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return "{}".format(self.pk)


# class Preference(models.Model):
#     preferenceSlug = models.SlugField(unique=True, max_length=200, editable=False)
#     preferenceType = models.CharField(max_length=100, help_text="eg Quiet hours")

#     def __str__(self):
#         return self.preferenceType

class RoommatePost(models.Model):

    student = models.ForeignKey(UserStudent, related_name='student', on_delete=models.CASCADE)
    # preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    # interest = models.ManyToManyField(Interest)
    image = models.ImageField(upload_to=roompost_image_file_path, blank=True)
    image1 = models.ImageField(upload_to=roompost_image_file_path, blank=True)
    image2 = models.ImageField(upload_to=roompost_image_file_path, blank=True)
    image3 = models.ImageField(upload_to=roompost_image_file_path, blank=True)
    heart = models.ManyToManyField(UserStudent, related_name="hearts", blank=True)
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    @property
    def totalHearts(self):
        return self.heart.count

    def __str__(self):
        return self.title


class PostComment(models.Model):

    roomatePost = models.ForeignKey(RoommatePost, related_name='comments', on_delete=models.CASCADE)
    student = models.ForeignKey(UserStudent, related_name='commentedstudent', on_delete=models.CASCADE)
    comment = models.TextField()
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['createdDate']


class CommentReply(models.Model):

    comment = models.ForeignKey(PostComment, related_name='commentreply', on_delete=models.CASCADE)
    student = models.ForeignKey(UserStudent, related_name='repliedstudent', on_delete=models.CASCADE)
    reply = models.TextField()
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['createdDate']

    def __str__(self):
        return self.reply


# Signals and receivers of models here
# @receiver(pre_save, sender=Preference)
# def auto_add_unique_slug_field_preference(sender, instance, **kwargs):
#     """
#     Automatically add unique slug field to the Preference models
#     """
#     if instance.preferenceSlug:
#         prop = Preference.objects.get(pk=instance.pk)
#         if instance.preferenceType != prop.preferenceType:
#             instance.preferenceSlug = unique_slug_generator_preference(instance)
#     if not instance.preferenceSlug:
#         instance.preferenceSlug = unique_slug_generator_preference(instance)

# @receiver(pre_save, sender=RoommatePost)
# def auto_delete_roommate_post_images_if_modified(sender, instance, **kwargs):
#     """
#     Deletes roommates post images file from filesystem
#     when corresponding MediaFile is modified.
#     """
#     alreadyExists = RoommatePost.objects.filter(pk=instance.pk).exists()
#     if alreadyExists:
#         oldFile = RoommatePost.objects.get(pk=instance.pk)
#         if instance.image:
#             if str(oldFile.image) != str(instance.image) and (str(oldFile.image) != ''):
#                 if os.path.isfile(oldFile.image.path):
#                     os.remove(oldFile.image.path)
#         else:
#             if oldFile.image:
#                 if os.path.isfile(oldFile.image.path):
#                     os.remove(oldFile.image.path)
#         if instance.image1:
#             if str(oldFile.image1) != str(instance.image1) and (str(oldFile.image1) != ''):
#                 if os.path.isfile(oldFile.image1.path):
#                     os.remove(oldFile.image1.path)
#         else:
#             if oldFile.image1:
#                 if os.path.isfile(oldFile.image1.path):
#                     os.remove(oldFile.image1.path)
#         if instance.image2:
#             if str(oldFile.image2) != str(instance.image2) and (str(oldFile.image2) != ''):
#                 if os.path.isfile(oldFile.image2.path):
#                     os.remove(oldFile.image2.path)
#         else:
#             if oldFile.image2:
#                 if os.path.isfile(oldFile.image2.path):
#                     os.remove(oldFile.image2.path)
#         if instance.image3:
#             if str(oldFile.image3) != str(instance.image3) and (str(oldFile.image3) != ''):
#                 if os.path.isfile(oldFile.image3.path):
#                     os.remove(oldFile.image3.path)
#         else:
#             if oldFile.image3:
#                 if os.path.isfile(oldFile.image3.path):
#                     os.remove(oldFile.image3.path)

# @receiver(post_delete, sender=RoommatePost)
# def auto_delete_seller_profile_pic_on_delete(sender, instance, **kwargs):
#     """
#     Deletes roommates post images file from filesystem
#     when corresponding MediaFile is deleted.
#     """
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)
#     if instance.image1:
#         if os.path.isfile(instance.image1.path):
#             os.remove(instance.image1.path)
#     if instance.image2:
#         if os.path.isfile(instance.image2.path):
#             os.remove(instance.image2.path)
#     if instance.image3:
#         if os.path.isfile(instance.image3.path):
#             os.remove(instance.image3.path)