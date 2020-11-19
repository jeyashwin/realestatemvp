from rest_framework import serializers

from chat.models import Room, MessageRequest
from .models import RoommatePost, PostComment, CommentReply


class StudentSerializer(serializers.RelatedField):
    def to_representation(self, value):
        friendStatus = {'status': 'CurrentUser'} 
        loggedUser = self.context['request'].user
        if value.user.user != loggedUser:
            if loggedUser.usertype.userstudent.friend.friends.filter(user=value.user).exists():
                room = Room.objects.filter(room_type=False).filter(members=loggedUser).filter(members=value.user.user).first()
                friendStatus['status'] = 'Friends'
                friendStatus['url'] = room.pk
            elif MessageRequest.objects.filter(logged_in_user=loggedUser.usertype.userstudent).filter(request_sender=value).filter(status=False):
                print(MessageRequest.objects.filter(logged_in_user=loggedUser.usertype.userstudent).filter(request_sender=value).filter(status=False))
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


class CommentReplySerializer(serializers.ModelSerializer):
    """Serializer for CommentReply"""
    student = StudentSerializer(read_only=True)

    class Meta:
        model = CommentReply
        fields = ['id', 'comment', 'student', 'reply', 'updateDate', 'createdDate']
        read_only_fields = ['id', 'comment', 'student', 'updateDate', 'createdDate']


class PostCommentSerializer(serializers.ModelSerializer):
    """Serializer for PostComment"""
    commentreply = CommentReplySerializer(many=True, read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'roomatePost', 'student', 'comment', 'updateDate', 'createdDate', 'commentreply']
        read_only_fields = ['id', 'roomatePost', 'student', 'commentreply', 'updateDate', 'createdDate']


class RoommatePostSerializer(serializers.ModelSerializer):
    """Serializer for RoommatePost create & update"""
    class Meta:
        model = RoommatePost
        # fields = ['id', 'title', 'description', 'interest', 'image', 'image1', 'image2', 'image3']
        fields = ['id', 'title', 'description', 'image', 'image1', 'image2', 'image3']


class RoommatePostDetailSerializer(serializers.ModelSerializer):
    """Serializer for RoommatePost Detail"""
    student = StudentSerializer(read_only=True)
    # interest = serializers.StringRelatedField(many=True)
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = RoommatePost
        # fields = ['id', 'student', 'preference', 'title', 'description', 'interest', 'image', 'image1', 'image2', 'image3', 'totalHearts', 'comments', 'updateDate', 'createdDate']
        # read_only_fields = ['id', 'student', 'preference', 'interest', 'comments', 'updateDate', 'createdDate']
        fields = ['id', 'student', 'title', 'description', 'image', 'image1', 'image2', 'image3', 'totalHearts', 'comments', 'updateDate', 'createdDate']
        read_only_fields = ['id', 'student', 'comments', 'updateDate', 'createdDate']