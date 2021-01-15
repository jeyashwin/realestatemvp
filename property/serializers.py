from rest_framework import serializers
from .models import StateList, CityList, Amenities, Property, PropertyImage, PropertyVideo, PropertyNearby, PropertyJobStore, PostQuestion, PostAnswer

class StateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateList
        fields = ('stateFullName', 'stateShortName')

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityList
        fields = ('state', 'cityName')

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ('amenityType')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('landlord', 'urlSlug', 'title', 'city', 'zipcode', 'address', 'location', 'locationType', 'averageDistance', 'placeId', 'sqft',
                  'occupants', 'rooms', 'bathrooms', 'securityDeposit', 'amount', 'rent', 'description', 'garage', 'parkingSpace', 'amenities',
                  'fromDate', 'toDate', 'likes', 'dislikes', 'isleased', 'leaseStart', 'leaseEnd', 'updatedDate', 'createdDate')

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('propertyKey')

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ('propertyKey', 'videoDescription', 'videoPath')

class PropertyNearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyNearby
        fields = ('propObject', 'nearByType', 'nearByName', 'location', 'placeId', 'distanceToProp')

class PropertyJobStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyJobStore
        fields = ('propObject', 'jobid', 'address', 'updatedDate')

class PostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostQuestion
        fields = ('propKey', 'student', 'question', 'createdDate')

class PostAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAnswer
        fields = ('question', 'answer', 'createdDate')
