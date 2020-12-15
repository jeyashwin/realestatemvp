from rest_framework import serializers

from chat.models import Room, MessageRequest, Friend
from .models import DiscussionPost, DiscussionPostComment, DiscussionCommentReply


class StudentSerializer(serializers.RelatedField):
    def to_representation(self, value):
        friendStatus = {'status': 'CurrentUser'} 
        loggedUser = self.context['request'].user
        if value.user.user != loggedUser:
            if Friend.objects.filter(student__user=loggedUser.usertype).exists() and loggedUser.usertype.userstudent.friend.friends.filter(user=value.user).exists():
                room = Room.objects.filter(room_type=False).filter(members=loggedUser).filter(members=value.user.user).first()
                friendStatus['status'] = 'Friends'
                friendStatus['url'] = room.pk
            elif MessageRequest.objects.filter(logged_in_user=loggedUser.usertype.userstudent).filter(request_sender=value).filter(status=False):
                # print(MessageRequest.objects.filter(logged_in_user=loggedUser.usertype.userstudent).filter(request_sender=value).filter(status=False))
                friendStatus['status'] = 'FriendRequestSent'
            else:
                friendStatus['status'] = 'NotFriends'
        interests = []
        for interest in value.interests.all():
            interests.append(interest.interest)
        
        if value.profilePicture != "":
            image = value.profilePicture.url
        else:
            image = None
        data = {
            'name': "{} {}".format(value.user.user.first_name, value.user.user.last_name),
            'email': value.user.user.email,
            'image': image,
            'interest': interests,
            'username': value.user.user.username,
            'sleepScheduleFrom': value.sleepScheduleFrom,
            'sleepScheduleTo': value.sleepScheduleTo,
            'studyHourFrom': value.studyHourFrom,
            'studyHourTo': value.studyHourTo,
            'tobaccoUsage': value.tobaccoUsage,
            'alcoholUsage': value.alcoholUsage,
            'cleanliness': value.cleanliness,
            'guests': value.guests,
            'friendStatus': friendStatus
        }
        return data


class DiscussionCommentReplySerializer(serializers.ModelSerializer):
    """Serializer for DiscussionCommentReply"""
    student = StudentSerializer(read_only=True)

    class Meta:
        model = DiscussionCommentReply
        fields = ['id', 'comment', 'student', 'reply', 'updateDate', 'createdDate']
        read_only_fields = ['id', 'comment', 'student', 'updateDate', 'createdDate']


class DiscussionPostCommentSerializer(serializers.ModelSerializer):
    """Serializer for DiscussionPostComment"""
    commentreply = DiscussionCommentReplySerializer(many=True, read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = DiscussionPostComment
        fields = ['id', 'discussionPost', 'student', 'comment', 'updateDate', 'createdDate', 'commentreply']
        read_only_fields = ['id', 'discussionPost', 'student', 'commentreply', 'updateDate', 'createdDate']


class DiscussionPostSerializer(serializers.ModelSerializer):
    """Serializer for DiscussionPost create & update"""
    class Meta:
        model = DiscussionPost
        fields = ['id', 'title', 'description', 'tags', 'image']


class DiscussionPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for DiscussionPost Detail"""
    student = StudentSerializer(read_only=True)
    tags = serializers.StringRelatedField(many=True)
    comments = DiscussionPostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = DiscussionPost
        fields = ['id', 'student', 'title', 'description', 'tags', 'image', 'totalHearts', 'comments', 'updateDate', 'createdDate']
        read_only_fields = ['id', 'student', 'comments', 'updateDate', 'createdDate']