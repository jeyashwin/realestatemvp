from django.contrib import admin
from .models import UserStudent, UserLandLord, UserType, Interest, InviteCode, ContactUS, PhoneVerification

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

@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'inviteCode')
    readonly_fields = ['createdDate']

@admin.register(ContactUS)
class UserLandLordAdmin(admin.ModelAdmin):
    list_display = ('id', 'contactEmail', 'subject')
    readonly_fields = ['createdDate']

admin.site.register(PhoneVerification)