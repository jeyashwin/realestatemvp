from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(DiscussionTag)
class DiscussionTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag']


@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'title']
    readonly_fields = ['heart', 'totalHearts', 'updateDate', 'createdDate']


@admin.register(DiscussionPostComment)
class DiscussionPostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'discussionPost', 'student', 'comment']
    readonly_fields = ['updateDate', 'createdDate']


@admin.register(DiscussionCommentReply)
class DiscussionCommentReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'student', 'reply']
    readonly_fields = ['updateDate', 'createdDate']

