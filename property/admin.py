from django.contrib import admin
from .models import PROPERTY,MEDIA
from django.contrib.sessions.models import Session

# Register your models here.

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self,obj):
        return obj.get_decoded()
    list_display=['session_key','_session_data','expire_date']

admin.site.register(PROPERTY)
admin.site.register(MEDIA)
admin.site.register(Session,SessionAdmin)