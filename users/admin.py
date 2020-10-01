from django.contrib import admin
from .models import UserStudent, UserLandLord, UserType, Interest

# Register your models here.

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'student','landLord')
    readonly_fields = ['student','landLord']

@admin.register(UserStudent)
class UserStudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'university', 'classYear', 'emailVerified', 'phoneVerified')

@admin.register(UserLandLord)
class UserLandLordAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'emailVerified', 'phoneVerified')

@admin.register(Interest)
class UserLandLordAdmin(admin.ModelAdmin):
    list_display = ('interest',)

