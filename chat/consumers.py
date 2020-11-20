# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Room
from notifications.models import Notification
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .views import get_user_contact

class ChatConsumer(WebsocketConsumer):

    def message_to_json(self, message):
        if len(message.content) == 0:
            return {
                'author': message.author.username,
                'content': str(message.pdf), 
                'timestamp': str(message.timestamp),
            }
        else:
            return {
                'author': message.author.username,
                'content': message.content, 
                'timestamp': str(message.timestamp),
            }

    
    def messages_to_json(self, messages):
        """Function that serialize messages object to json"""
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result


    def fetch_messages(self, data):
        messages = Message.objects.filter(room__id = data['roomname']).order_by('timestamp')
        content = {
            'message': self.messages_to_json(messages),
            'command': 'fetch_messages'
        }

        self.send_message(content)


    def new_message(self, data):
        author = data['from']
        room_id = data['roomname']
        room_id_valid = get_object_or_404(Room, id=room_id)

        if len(data['message']) != 0:
            message = Message.objects.create(
                author = get_object_or_404(User, username=author),
                content = data['message'],
                room = room_id_valid
            )
            authorMember = get_object_or_404(User, username=author)
            for member in room_id_valid.members.exclude(username=authorMember.username):
                if Notification.objects.filter(fromUser=authorMember, toUser=member, notificationType='newMessage', viewed=False, identifier=room_id_valid.pk).exists():
                    notfi = Notification.objects.filter(fromUser=authorMember, toUser=member, notificationType='newMessage', viewed=False, identifier=room_id_valid.pk).first()
                    count = int(notfi.content)
                    notfi.content = count+1
                    notfi.save()
                else:
                    notfi = Notification.objects.create(
                                fromUser=authorMember, 
                                toUser=member,
                                notificationType='newMessage', 
                                content=1,
                                identifier=room_id_valid.pk,
                            )
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
        else:
            message = get_object_or_404(Message, pk=data['message_id'])
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
        return self.send_chat_messages(content)

    command = {
        'fetch_messages': fetch_messages, 
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print(data, "!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.command[data["command"]](self, data)

    def send_chat_messages(self, message):
        # Send message to room group
        try:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except Exception as e:
            print(e)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))