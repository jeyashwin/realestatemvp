from rest_framework import serializers

from .models import RoommatePost, PostImage, PostComment, CommentReply


class StudentSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if value.profilePicture != "":
            image = value.profilePicture.url
        else:
            image = None
        data = {
            'name': "{} {}".format(value.user.user.first_name, value.user.user.last_name),
            'email': value.user.user.email,
            'image': image,
            'username': value.user.user.username
        }
        return data


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer for PostImage"""

    class Meta:
        model = PostImage
        fields = ['id', 'roommatePost', 'image']
        read_only_fields = ['id', 'roommatePost']


class CommentReplySerializer(serializers.ModelSerializer):
    """Serializer for CommentReply"""
    student = StudentSerializer(read_only=True)

    class Meta:
        model = CommentReply
        fields = ['id', 'comment', 'student', 'mention', 'reply', 'updateDate', 'createdDate']
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
    """Serializer for RoommatePost"""
    student = StudentSerializer(read_only=True)
    interest = serializers.StringRelatedField(many=True)
    roommateimages = PostImageSerializer(many=True, read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = RoommatePost
        fields = ['id', 'student', 'title', 'description', 'interest', 'roommateimages', 'comments', 'updateDate', 'createdDate']
        read_only_fields = ['id', 'student', 'interest', 'comments', 'updateDate', 'createdDate']