from django.db import models

from users.models import UserStudent, Interest
from property.models import Property
# Create your models here.

class Favourite(models.Model):

    student = models.OneToOneField(UserStudent, related_name="favourites", on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return "{}".format(self.pk)


class RoommatePost(models.Model):

    student = models.ForeignKey(UserStudent, related_name='student', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    interest = models.ManyToManyField(Interest)
    heart = models.ManyToManyField(UserStudent, related_name="hearts", blank=True)
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):

    roommatePost = models.ForeignKey(RoommatePost, related_name='roommateimages', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/post/')

    def __str__(self):
        return '{}'.format(self.pk)


class PostComment(models.Model):

    roomatePost = models.ForeignKey(RoommatePost, related_name='comments', on_delete=models.CASCADE)
    student = models.ForeignKey(UserStudent, related_name='commentedstudent', on_delete=models.CASCADE)
    comment = models.TextField()
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class CommentReply(models.Model):

    comment = models.ForeignKey(PostComment, related_name='commentreply', on_delete=models.CASCADE)
    student = models.ForeignKey(UserStudent, related_name='repliedstudent', on_delete=models.CASCADE)
    mention = models.ManyToManyField(UserStudent, related_name='mention', blank=True)
    reply = models.TextField()
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply