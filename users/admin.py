from django.contrib import admin
from .models import UserBuyer, UserLandLord

# Register your models here.

admin.site.register(UserBuyer)
admin.site.register(UserLandLord)
