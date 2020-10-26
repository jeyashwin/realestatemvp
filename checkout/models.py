from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

import datetime, phonenumbers

from property.models import Property
from services.models import Service
from users.models import UserStudent
# Create your models here.


class RequestToRentProperty(models.Model):

    StatusChoices = [
        ('pending', 'Pending'),
        ('viewed', 'Viewed')
    ]

    propertyObj = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='Property')
    studentObj = models.ForeignKey(UserStudent, on_delete=models.CASCADE, verbose_name='Student')
    occupants = models.IntegerField(help_text="Number of people will stay", validators=[
                    MinValueValidator(1, "Minimum 1"),
                    MaxValueValidator(20, "Maximum 20")
                ], )
    moveIn = models.DateField()
    moveOut = models.DateField()
    status = models.CharField(max_length=50, choices=StatusChoices, default='pending')
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.pk)
    
    def clean(self):
        errorMess = {}
        if self.occupants > self.propertyObj.occupants:
            errorMess['occupants'] = ValidationError(('Entered occupants greater than the property can contain.'), code='invalid1')

        if self.moveIn is not None:
            if self.moveIn < datetime.date.today():
                errorMess['moveIn'] = ValidationError(('Move In cannot be older than today.'), code='error')
        
        if self.moveOut is not None:
            if self.moveOut <= self.moveIn:
                errorMess['moveOut'] = ValidationError(('Move Out should be greater than Move In.'), code='error')

        if errorMess is not None:
            raise ValidationError(errorMess)


class RequestToRentService(models.Model):

    StatusChoices = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered')
    ]

    serviceObj = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Service')
    studentObj = models.ForeignKey(UserStudent, on_delete=models.CASCADE, verbose_name='Student')
    fromDate = models.DateField()
    toDate = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(region='US')
    email = models.EmailField(max_length=254)
    deliveryAddress = models.TextField()
    status = models.CharField(max_length=50, choices=StatusChoices, default='pending')
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
    def clean(self):
        errorMess = {}

        if self.fromDate is not None:
            if self.fromDate < datetime.date.today():
                errorMess['fromDate'] = ValidationError(('From Date cannot be older than today.'), code='error')
        
        if self.toDate is not None:
            if self.toDate <= self.fromDate:
                errorMess['toDate'] = ValidationError(('To Date should be greater than From Date.'), code='error')

        try:
            phone = phonenumbers.parse(str(self.phone_number), None)
            if phone.country_code != 1:
                # print(phone.country_code)
                # print(type(phone.country_code))
                errorMess['phone_number'] = ValidationError(('Currently we accept only USA Numbers!'), code='invalid phone')
        except phonenumbers.NumberParseException:
            pass

        if errorMess is not None:
            raise ValidationError(errorMess)