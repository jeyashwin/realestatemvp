from django.contrib import admin

from .models import Message, MessageRequest, Room, Friend

admin.site.register(Message)
admin.site.register(MessageRequest)
admin.site.register(Room)
admin.site.register(Friend)