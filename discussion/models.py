from django.db import models

from users.models import UserStudent

import uuid, os

# Create your models here.

def discussion_image_file_path(instance, filename):
    """Generate file path for new discussion post image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/discussion/', filename)


class DiscussionTag(models.Model):

    tag = models.CharField(max_length=100, help_text="eg Shops, Food places")

    def __str__(self):
        return self.tag


class DiscussionPost(models.Model):

    student = models.ForeignKey(UserStudent, related_name='studentDiscussion', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    tags = models.ManyToManyField(DiscussionTag)
    image = models.ImageField(upload_to=discussion_image_file_path, blank=True)
    heart = models.ManyToManyField(UserStudent, related_name="Discussionhearts", blank=True)
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    @property
    def totalHearts(self):
        return self.heart.count

    def __str__(self):
        return self.title


class DiscussionPostComment(models.Model):

    discussionPost = models.ForeignKey(DiscussionPost, related_name='comments', on_delete=models.CASCADE)
    student = models.ForeignKey(UserStudent, on_delete=models.CASCADE)
    comment = models.TextField()
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['createdDate']


class DiscussionCommentReply(models.Model):

    comment = models.ForeignKey(DiscussionPostComment, related_name='commentreply', on_delete=models.CASCADE)
    student = models.ForeignKey(UserStudent, on_delete=models.CASCADE)
    reply = models.TextField()
    updateDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['createdDate']

    def __str__(self):
        return self.reply