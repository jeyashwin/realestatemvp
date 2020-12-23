from django.urls import path
from .views import *

app_name = "discussion"

urlpatterns = [
    path('social/', DiscussionListView.as_view(), name="discussionList"),
    
    path('discussion/post/create/', DiscussionPostCreateView.as_view(), name="discussionCreate"),
    path('discussion/post/<int:pk>/update/', DiscussionPostUpdateDeleteView.as_view(), name="discussionUpdate"),
    path('discussion/post/<int:pk>/', DiscussionPostDetailView.as_view(), name="discussionDetail"),
    path('discussion/post/<int:pk>/delete/', DiscussionPostUpdateDeleteView.as_view(), name="discussionDelete"),

    path('discussion/post/<int:pk>/heart/', DiscussionAddRemoveHeart, name="discussionAddRemoveHeart"),

    path('discussion/<int:pk>/comment/create/', DiscussionPostCommentCreateView.as_view(), name="discussionCommentCreate"),
    path('discussion/comment/<int:pk>/', DiscussionPostCommentUpdateDeleteView.as_view(), name="discussionCommentUpdateDelete"),

    path('discussion/comment/<int:pk>/reply/create/', DiscussionCommentReplyCreateView.as_view(), name="discussionReplyCreate"),
    path('discussion/reply/<int:pk>/', DiscussionCommentReplyUpdateDeleteView.as_view(), name="replyUpdateDelete"),
]
