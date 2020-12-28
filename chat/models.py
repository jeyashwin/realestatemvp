from django.db import models
from django.contrib.auth import get_user_model
from users.models import UserStudent
from django.dispatch import receiver

import uuid, os

User = get_user_model()


def unique_file_path_generator_chat(instance, filename):
    """Generate file path for chat attachments"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    filepath = ("uploads/chat/{roomid}/").format(
                    roomid=instance.room.pk, 
                )
    return os.path.join(filepath, filename)


class Room(models.Model):

    name = models.CharField(max_length = 50, blank=True, null=True)
    members = models.ManyToManyField(User, related_name='members')
    room_type = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pk)


class Message(models.Model):

    author = models.ForeignKey(User, related_name="author_message", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name="room", on_delete=models.CASCADE, null=True)
    pdf = models.FileField(upload_to=unique_file_path_generator_chat, null=True, blank=True)
    # pdf = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.author.username
        

class MessageRequest(models.Model):

    logged_in_user = models.ForeignKey(UserStudent,  related_name = 'message_user', on_delete=models.CASCADE)
    request_sender = models.ForeignKey(UserStudent, related_name = 'message_request_sender', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.request_sender.user.user.username


class Friend(models.Model):
    student = models.OneToOneField(UserStudent, on_delete=models.CASCADE)
    friends = models.ManyToManyField(UserStudent, related_name='friendsList')
    # from_friend = models.ForeignKey(UserStudent, related_name='from_friends', on_delete=models.CASCADE, blank=True, null=True)
    # to_friend = models.ForeignKey(UserStudent, related_name='to_friends', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pk)
