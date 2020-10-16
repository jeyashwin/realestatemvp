from django.contrib import admin
from .models import Favourite, RoommatePost, PostComment, CommentReply, Preference

# Register your models here.
@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ["id", "student"]


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'preferenceType']
    readonly_fields = ['preferenceSlug',]


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