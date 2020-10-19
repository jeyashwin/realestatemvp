from django.contrib import admin

from .models import *
# Register your models here.

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['serviceName', 'rentCycle', 'price']
    inlines = [ServiceImageInline]