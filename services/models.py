from django.db import models
from django.core.validators import MinValueValidator

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