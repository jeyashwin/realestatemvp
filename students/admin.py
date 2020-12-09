from django.contrib import admin
# from .models import Favorite, RoommatePost, PostComment, CommentReply, Preference
from .models import RoommatePost, PostComment, CommentReply

# Register your models here.
# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ["id", "student"]


# @admin.register(Preference)
# class PreferenceAdmin(admin.ModelAdmin):
#     list_display = ['id', 'preferenceType']
#     readonly_fields = ['preferenceSlug',]


@admin.register(RoommatePost)
class RoommatesPostAdmin(admin.ModelAdmin):
    list_display = ['student', 'title']
    readonly_fields = ['heart', 'totalHearts', 'updateDate', 'createdDate']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['roomatePost', 'student']
    

@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['comment', 'student']