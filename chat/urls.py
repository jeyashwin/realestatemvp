from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('message_request/', message_request_update, name='message_request_update'),
    path('message_request_list/', RequestView.as_view(), name='message_request_list'),
    path('create/', create_room, name='create_room'),
    path('create_group/', CreateGroupView.as_view(), name='creategroup'),
    path('groups/', index_group, name='groupindex'),
    path('group/<int:room_name>/', group, name="group"),
    path('room/<int:room_name>/', room, name='room'),
    path('create/<slug:slug>/', landlord_chat, name='landlordchat'),
]
