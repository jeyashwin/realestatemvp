from django.db import models

# Create your models here.

class Notification(models.Model):

    NotificationChoice = [
        ('rentRequest', 'Property Rent Request'),
    ]

    fromObject = models.CharField(max_length=250)
    toObject = models.CharField(max_length=250)
    notificationType = models.CharField(max_length=100, choices=NotificationChoice)
    identifier = models.CharField(max_length=300)
    viewed = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fromObject