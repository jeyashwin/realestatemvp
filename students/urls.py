from django.urls import path
from .views import *


app_name = 'students'

urlpatterns = [
    path('favourites/', FavouriteListView.as_view(), name="favourites"),
    path('favourites/add/<slug:slug>/', AddFavourite, name="addFavourites"),
    path('favourites/remove/<slug:slug>/', RemoveFavourite, name="removeFavourites"),

    path('roommates/', RoommatesListView.as_view(), name="roommates"),
    path('roommates/mypost/', RoommatesMyPostListView.as_view(), name="roommatesMypost"),
    
    #enable if preferences
    # path('roommates/<slug:preference>/', RoommatesListView.as_view(), name="roommatesPreference"),
    # path('roommates/<slug:preference>/post/create/', RoommatesPostCreateView.as_view(), name="postCreate"),

    path('roommates/post/create/', RoommatesPostCreateView.as_view(), name="postCreate"),
    # path('roommates/post/<int:pk>/update/', PostUpdateView.as_view(), name="postUpdate"),
    path('roommates/post/<int:pk>/', RoommatesPostDetailView.as_view(), name="postDetail"),
    path('roommates/post/<int:pk>/delete/', RoommatesPostDeleteView.as_view(), name="postDelete"),

    path('roommates/post/<int:pk>/heart/', AddRemoveHeart, name="addRemoveHeart"),

    path('roommates/<int:pk>/comment/create/', PostCommentCreateView.as_view(), name="commentCreate"),
    path('roommates/comment/<int:pk>/', PostCommentUpdateDeleteView.as_view(), name="commentUpdateDelete"),

    path('roommates/comment/<int:pk>/reply/create/', CommentReplyCreateView.as_view(), name="replyCreate"),
    path('roommates/reply/<int:pk>/', CommentReplyUpdateDeleteView.as_view(), name="replyUpdateDelete"),

    path('roommates_groups', roommatesGroup, name='group'),
    path('roommates_messages', roommatesMessage, name='message'),
]