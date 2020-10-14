from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

from users.models import UserStudent, Interest
from property.models import Property
from .utils import unique_slug_generator_preference
# Create your models here.

class Favourite(models.Model):

    student = models.OneToOneField(UserStudent, related_name="favourites", on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return "{}".format(self.pk)


class Preference(models.Model):
    preferenceSlug = models.SlugField(unique=True, max_length=200, editable=False)
    preferenceType = models.CharField(max_length=100, help_text="eg Quiet hours")

    def __str__(self):
        return self.preferenceType

class RoommatePost(models.Model):

    student = models.ForeignKey(UserStudent, related_name='student', on_delete=models.CASCADE)
    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    interest = models.ManyToManyField(Interest)
    image = models.ImageField(upload_to='uploads/post/')
    image1 = models.ImageField(upload_to='uploads/post/')
    image2 = models.ImageField(upload_to='uploads/post/')
    image3 = models.ImageField(upload_to='uploads/post/', blank=True)
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
@receiver(pre_save, sender=Preference)
def auto_add_unique_slug_field_preference(sender, instance, **kwargs):
    """
    Automatically add unique slug field to the Preference models
    """
    if instance.preferenceSlug:
        prop = Preference.objects.get(pk=instance.pk)
        if instance.preferenceType != prop.preferenceType:
            instance.preferenceSlug = unique_slug_generator_preference(instance)
    if not instance.preferenceSlug:
        instance.preferenceSlug = unique_slug_generator_preference(instance)