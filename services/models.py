from django.db import models

# Create your models here.


class Service(models.Model):

    serviceName = models.CharField(max_length=50, help_text='Eg Bed, TV etc')
    description = models.TextField()
    dutaion = models.DurationField()
    rentCycle = models.CharField(max_length=50, 
                    choices=[
                        ('weekly', 'Weekly'),
                        ('monthly', 'Monthly'),
                        ('yearly', 'Yearly'),
                    ]
                )
    price = models.IntegerField()

    def __str__(self):
        return "{}".format(self.pk)