from django.db import models
from django.contrib.auth import get_user_model
from users.models import UserStudent
from django.dispatch import receiver

User = get_user_model()


class Room(models.Model):

    name = models.CharField(max_length = 50, blank=True, null=True)
    members = models.ManyToManyField(UserStudent, related_name='members')
    room_type = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pk)


class Message(models.Model):

    author = models.ForeignKey(UserStudent, related_name="author_message", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name="room", on_delete=models.CASCADE, null=True)
    pdf = models.FileField(null=True, blank=True)
    # pdf = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.author.user.user.username




class MessageRequest(models.Model):

    logged_in_user = models.ForeignKey(UserStudent,  related_name = 'message_user', on_delete=models.CASCADE)
    request_sender = models.ForeignKey(UserStudent, related_name = 'message_request_sender', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.request_sender.user.user.username


class Favorites(models.Model):
    from_friend = models.ForeignKey(UserStudent, related_name='from_friends', on_delete=models.CASCADE, blank=True, null=True)
    to_friend = models.ForeignKey(UserStudent, related_name='to_friends', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pk)




