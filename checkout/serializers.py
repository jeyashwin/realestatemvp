from rest_framework import serializers
from .models import RequestToRentProperty, RequestToRentService, RequestToTourProperty

class RequestToRentPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestToRentProperty
        fields = ('StatusChoices', 'propertyObj', 'studentOb', 'occupants', 'moveIn', 'moveOut', 'status', 'createdDate', 'updatedDate')


class RequestToRentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestToRentService
        fields = ('StatusChoices', 'serviceObj', 'studentObj', 'fromDate', 'toDate', 'first_name', 'last_name', 'phone_number', 'email', 'deliveryAddress', 'status', 'createdDate', 'updatedDate')

class RequestToTourPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestToTourProperty
        fields = ('propertyObj', 'studentObj', 'preference1Date', 'preference1Time', 'preference2Date', 'preference2Time', 'preference3Date', 'preference3Time', 'status', 'createdDate', 'updatedDate')

