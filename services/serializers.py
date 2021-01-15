from rest_framework import serializers
from .models import Service, ServiceImage

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('serviceName', 'rentCycle', 'price', 'createdDate')

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ('service', 'image')