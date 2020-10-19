from django.db import models
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

import uuid, os

# Create your models here.

def service_image_file_path(instance, filename):
    """Generate file path for new service image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/services/', filename)


class Service(models.Model):

    serviceName = models.CharField(max_length=50, help_text='Eg Bed, TV etc')
    description = models.TextField()
    rentCycle = models.CharField(max_length=50, 
                    choices=[
                        ('weekly', 'Weekly'),
                        ('monthly', 'Monthly'),
                        ('yearly', 'Yearly'),
                    ]
                )
    price = models.IntegerField(help_text="Amount in $", 
                validators=[MinValueValidator(0, 'Minimum Price cannot be lower than 0')]
            )
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.serviceName


class ServiceImage(models.Model):

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=service_image_file_path)

    def __str__(self):
        return "{}".format(self.pk)


# Signals and receivers of models here
@receiver(pre_save, sender=ServiceImage)
def auto_delete_service_image_on_modified(sender, instance, **kwargs):
    """
    Deletes Service image file from filesystem
    when corresponding MediaFile object is modified.
    """
    if instance.image:
        alreadyExists = ServiceImage.objects.filter(pk=instance.pk).exists()
        if alreadyExists:
            oldFile = ServiceImage.objects.get(pk=instance.pk)
            if str(oldFile.image) != str(instance.image):
                if os.path.isfile(oldFile.image.path):
                    os.remove(oldFile.image.path)

@receiver(post_delete, sender=ServiceImage)
def auto_delete_service_image_on_delete(sender, instance, **kwargs):
    """
    Deletes service image file from filesystem
    when corresponding MediaFile object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)