from rest_framework import serializers
from .models import UserType, Interest, UserStudent, UserLandLord, InviteCode, PhoneVerification, ContactUS

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('user', 'userType', 'student', 'landLord')

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('interest')

class UserStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStudent
        fields = ('usageChoices', 'user', 'phone', 'university', 'classYear', 'profilePicture', 'interests', 'fbLink',
                  'snapLink', 'instaLink', 'twitterLink', 'sleepScheduleFrom', 'sleepScheduleTo', 'studyHourFrom', 'studyHourTo',
                  'tobaccoUsage', 'alcoholUsage', 'cleanliness', 'guests', 'emailVerified', 'phoneVerified', 'livingHabitsLater', 'createdDate')

class UserLandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLandLord
        fields = ('user', 'phone', 'emailVerified', 'phoneVerified', 'createdDate')

class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = ('student', 'inviteCode', 'studentJoined', 'createdDate')

class PhoneVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerification
        fields = ('userObj', 'phone', 'wrongAttemptCount', 'resendCodeCount', 'is_blocked', 'createdDate', 'updatedDate')

class ContactUSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUS
        fields = ('contactEmail', 'subject', 'message', 'createdDate')
