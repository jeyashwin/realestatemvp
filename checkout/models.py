from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

import datetime, phonenumbers

from property.models import Property
from services.models import Service
from users.models import UserStudent
# Create your models here.

#validators
def validateIsTimeBetween(time):
    # print(time)
    # print(type(time))
    midNightStart = datetime.time(hour=23, minute=0, second=0)
    midNightEnd = datetime.time(hour=6, minute=0, second=0)
    # print(midNightStart)
    # print(type(midNightStart))
    # print(midNightEnd)
    # print(type(midNightEnd))
    if time >= midNightStart or time <= midNightEnd:
        raise ValidationError(_('Preferred Time cannot be in between 11PM to 6AM!.'),)

def validateDate(date):
    # print(date)
    if date < datetime.date.today():
        raise ValidationError(_('Preferred Date cannot be older than Today!.'),)

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


class RequestToTourProperty(models.Model):

    StatusChoices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('busy', 'Busy'),
    ]

    propertyObj = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name='Property')
    studentObj = models.ForeignKey(UserStudent, on_delete=models.CASCADE, verbose_name='Student')
    preference1Date = models.DateField(verbose_name='Date', validators=[validateDate])
    preference1Time = models.TimeField(verbose_name='Time', validators=[validateIsTimeBetween])
    preference2Date = models.DateField(verbose_name='Date', blank=True, null=True,
                        validators=[validateDate])
    preference2Time = models.TimeField(verbose_name='Time', blank=True, null=True, 
                        validators=[validateIsTimeBetween])
    preference3Date = models.DateField(verbose_name='Date', blank=True, null=True, 
                        validators=[validateDate])
    preference3Time = models.TimeField(verbose_name='Time', blank=True, null=True, 
                        validators=[validateIsTimeBetween])
    status = models.CharField(max_length=50, choices=StatusChoices, default='pending')
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.pk)
    
    def clean(self):
        errorMess = {}

        if self.preference2Date is not None and self.preference2Time is None:
            errorMess['preference2Time'] = ValidationError(('Time field is required!'), code='required')
        if self.preference2Date is None and self.preference2Time is not None:
            errorMess['preference2Date'] = ValidationError(('Date field is required!'), code='required')

        if self.preference3Date is not None and self.preference3Time is None:
            errorMess['preference3Time'] = ValidationError(('Time field is required!'), code='required')
        if self.preference3Date is None and self.preference3Time is not None:
            errorMess['preference3Date'] = ValidationError(('Date field is required!'), code='required')

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