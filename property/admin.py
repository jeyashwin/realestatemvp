from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import *

# Register your models here.
@admin.register(StateList)
class StateListAdmin(admin.ModelAdmin):
    list_display = ['stateFullName', 'stateShortName']


@admin.register(CityList)
class CityListAdmin(admin.ModelAdmin):
    list_display = ['state', 'cityName']


@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ['id', 'amenityType']


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    max_num = 10


class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1
    max_num = 4


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['landlord', 'title', 'city']
    readonly_fields = ['urlSlug', 'updatedDate', 'createdDate']
    fieldsets = [
        (None, {'fields': ['landlord', 'title', 'urlSlug']}),
        ('Location Information', {'fields': ['city', 'zipcode', 'address']}),
        ('Specfic Details', {'fields': ['sqft', 'occupants', 'rooms', 'bathrooms', 
                'securityDeposit', 'amount', 'rentPerPerson', 'description']}),
        ('Extra Information', {'fields': ['utilities', 'garage', 'parkingSpace', 'amenities']}),
        ('Availability Dates', {'fields': ['fromDate', 'toDate']}),
        ('Important Date Information', {'fields': ['updatedDate', 'createdDate']}),
    ]
    inlines = [PropertyImageInline, PropertyVideoInline]

# admin.site.register(PropertyImage)
# admin.site.register(PropertyVideo)
