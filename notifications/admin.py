from django.contrib import admin

from .models import Notification
# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'fromUser', 'toUser', 'notificationType', 'content', 'viewed']
    readonly_fields = ['createdDate', 'updatedDate']
    

