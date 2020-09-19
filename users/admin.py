from django.contrib import admin
from .models import UserBuyer, UserLandLord, UserType

# Register your models here.

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'buyer','landLord')
    readonly_fields = ['buyer','landLord']


class UserBuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'dateOfBirth', 'isStudent')


class UserLandLordAdmin(admin.ModelAdmin):
    list_display = ('user', 'dateOfBirth')


admin.site.register(UserType, UserTypeAdmin)
admin.site.register(UserBuyer, UserBuyerAdmin)
admin.site.register(UserLandLord, UserLandLordAdmin)
