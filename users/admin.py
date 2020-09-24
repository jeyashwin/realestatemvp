from django.contrib import admin
from .models import UserStudent, UserLandLord, UserType

# Register your models here.

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'student','landLord')
    readonly_fields = ['student','landLord']


class UserStudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'dateOfBirth', 'isCollegeStudent')


class UserLandLordAdmin(admin.ModelAdmin):
    list_display = ('user', 'dateOfBirth')


admin.site.register(UserType, UserTypeAdmin)
admin.site.register(UserStudent, UserStudentAdmin)
admin.site.register(UserLandLord, UserLandLordAdmin)
