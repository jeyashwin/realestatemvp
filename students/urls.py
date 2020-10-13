from django.urls import path
from .views import *


app_name = 'students'

urlpatterns = [
    path('favourites/', FavouriteListView.as_view(), name="favourites"),
    path('favourites/add/<slug:slug>/', AddFavourite, name="addFavourites"),
    path('favourites/remove/<slug:slug>/', RemoveFavourite, name="removeFavourites"),
    path('roommates/', RoommatesListView.as_view(), name="roommates"),
    path('roommates/<int:pk>/', RoommatesPostDetailDeleteView.as_view(), name="roommatesDetailDelete"),
    path('roommates/<int:pk>/comment/create/', PostCommentCreateView.as_view(), name="commentCreate"),
    path('roommates/comment/<int:pk>/', PostCommentUpdateDeleteView.as_view(), name="commentUpdateDelete"),
    path('roommates/comment/<int:pk>/reply/create/', CommentReplyCreateView.as_view(), name="replyCreate"),
    path('roommates/reply/<int:pk>/', CommentReplyUpdateDeleteView.as_view(), name="replyUpdateDelete"),
]