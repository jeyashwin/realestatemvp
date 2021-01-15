from rest_framework import serializers
from .models import Room, Message, MessageRequest, Friend

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'members', 'room_type')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('author', 'content', 'timestamp', 'room', 'pdf')

class MessageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRequest
        fields = ('logged_in_user', 'request_sender', 'status')

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('student', 'friends')
