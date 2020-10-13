from django.contrib import admin
from .models import Favourite, RoommatePost, PostImage, PostComment, CommentReply

# Register your models here.
@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ["id", "student"]


class RoomatePostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    max_num = 10


@admin.register(RoommatePost)
class RoommatesPostAdmin(admin.ModelAdmin):
    list_display = ['student', 'title']
    inlines = [RoomatePostImageInline]


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['roomatePost', 'student']
    

@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['comment', 'student']