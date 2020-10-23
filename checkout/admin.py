from django.contrib import admin

from .models import RequestToRentProperty

# Register your models here.

@admin.register(RequestToRentProperty)
class RequestToRentPropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'propertyObj', 'studentObj', 'occupants', 'moveIn', 'moveOut', 'status']
    readonly_fields = ['createdDate', 'updatedDate']

    # def has_delete_permission(self, request, obj=None):
    #     return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False