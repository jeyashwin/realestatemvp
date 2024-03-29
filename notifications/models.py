from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):

    NotificationChoice = [
        ('rentRequest', 'Property Rent Request'),
        ('tourRequest', 'Property Tour Request'),
        ('serviceRequest', 'Service Rent Request'),
        ('question', 'Asked Question'),
        ('answered', 'Question is answered'),
        ('deletedQuestion', 'Question is deleted'),
        ('newChatLandlord', 'New chat creation landlord'),
        ('newMessage', 'New chat Message'),
        ('newFriendRequest', 'New Friend request'),
        ('acceptFriendRequest', 'New Friend request Accepted'),
        ('denyFriendRequest', 'New Friend request Denyed'),
        ('tagFriend', 'Tag Friend'),
    ]

    fromUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fromUser')
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='toUser')
    notificationType = models.CharField(max_length=100, choices=NotificationChoice)
    content = models.CharField(max_length=250)
    identifier = models.CharField(max_length=300)
    viewed = models.BooleanField(default=False)
    updatedDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notificationType

    class Meta:
        ordering = ['-updatedDate']