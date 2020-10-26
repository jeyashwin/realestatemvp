from django.contrib import admin

from .models import RequestToRentProperty, RequestToRentService

# Register your models here.

@admin.register(RequestToRentProperty)
class RequestToRentPropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'propertyObj', 'studentObj', 'occupants', 'moveIn', 'moveOut', 'status']
    readonly_fields = ['createdDate', 'updatedDate']

    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(RequestToRentService)
class RequestToRentServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'serviceObj', 'studentObj', 'fromDate', 'toDate', 'first_name', 'status']
    readonly_fields = ['fromDate', 'toDate', 'first_name', 
                        'last_name', 'phone_number', 'email', 'deliveryAddress', 
                        'createdDate', 'updatedDate']

    fieldsets = [
        (None, {'fields': ['serviceObj', 'studentObj']}),
        ('Requested Dates', {'fields': ['fromDate', 'toDate']}),
        ('Location Information', {'fields': ['deliveryAddress']}),
        ('Buyer Details', {'fields': ['first_name', 'last_name', 'phone_number', 'email']}),
        ('Important Date Information', {'fields': ['updatedDate', 'createdDate']}),
        ('Current State', {'fields': ['status']}),
    ]

    def has_add_permission(self, request, obj=None):
        return False