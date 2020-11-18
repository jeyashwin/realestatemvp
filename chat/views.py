# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserStudent, Message, MessageRequest, Room, Friend
from users.models import UserType, UserLandLord
from property.models import Property
from notifications.models import Notification
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
import json

fs = FileSystemStorage(location='/home/pooja/Documents/Freelancing/realestatemvp/chatapp/static/uploads/')
fs.base_url = '/home/pooja/Documents/Freelancing/realestatemvp/chatapp/static/uploads/' 

User = get_user_model()


def get_user_contact(username):
    filter_user = get_object_or_404(User, username=username)
    filter_user_2 = get_object_or_404(UserType, user=filter_user)
    return get_object_or_404(UserStudent, user=filter_user_2)

@login_required
def index(request):
    if request.method == "GET":
        user_chats = []
        current_user_rooms = list(Room.objects.filter(room_type=False).filter(members__username = request.user).values_list('pk', flat=True))
        
        for room in Room.objects.filter(pk__in=current_user_rooms):
            name = room.members.exclude(username=request.user)[0]
            user_chats.append({
                'pk': room.pk,
                'name': name,
            })
        
        return render(request, "chat/room_index.html", {
            'user_chats':user_chats,
        })

@login_required
def index_group(request):
    if request.method == "GET":
        user_chats = []
        current_user_groups = list(Room.objects.filter(room_type=True).filter(members__username = request.user).values_list('pk', flat=True))
        
        for room in Room.objects.filter(pk__in=current_user_groups):
            name = room.name
            user_chats.append({
                'pk': room.pk,
                'name': name,
            })
        return render(request, "chat/group_index.html", {
            'user_chats':user_chats,
            'friends_list': Friend.objects.get(student__user__user=request.user),
        })


    
@login_required
def room(request, room_name):
    user_chats = []
    current_user_rooms = list(Room.objects.filter(room_type=False).filter(members__username = request.user).values_list('pk', flat=True))
        
    for room in Room.objects.filter(pk__in=current_user_rooms):
        name = room.members.exclude(username=request.user)[0]
        user_chats.append({
            'pk': room.pk,
            'name': name,
        })

    messages_room = Room.objects.filter(room_type=False).filter(members__username=request.user)
    room_details = get_object_or_404(messages_room, pk=room_name)
    another_member = ",".join(room_details.members.exclude(username=request.user).values_list('username', flat=True))
    
    if request.method == "POST":
        uploaded_file = request.FILES['myFile']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        new_message = Message.objects.create(
            room = get_object_or_404(Room, pk=room_name),
            author = request.user,
            content = '',
            pdf = url,
        )
        return JsonResponse({
                'room_id': room_name,
                'username': request.user.username,
                'url': url,
                'message_id': new_message.pk,
        })

    return render(request, 'chat/roommates_messages.html', {
        'user_chats': user_chats, 
        'another_member': another_member,
        'room_id': room_name,
        'username': request.user.username,
    })

@login_required
def group(request, room_name):

    user_chats = []
    current_user_rooms = list(Room.objects.filter(room_type=True).filter(members__username = request.user).values_list('pk', flat=True))
    
    for room in Room.objects.filter(pk__in=current_user_rooms):
        # name = room.members.exclude(user__user__username=request.user)[0]
        user_chats.append({
            'pk': room.pk,
            'name': room.name,
        })

    groups_room = Room.objects.filter(room_type=True).filter(members__username=request.user)
    room_details = get_object_or_404(groups_room, pk=room_name)
    another_member = ",".join(room_details.members.exclude(username=request.user).values_list('username', flat=True))

    if request.method == "POST":
        uploaded_file = request.FILES['myFile']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        new_message = Message.objects.create(
            room = get_object_or_404(Room, pk=room_name),
            author = request.user,
            content = '',
            pdf = url,
        )
        return JsonResponse({
                'room_id': room_name,
                'username': request.user.username,
                'url': url,
                'message_id': new_message.pk,
        })
       
    return render(request, 'chat/roommates_groups.html', {
        'user_chats': user_chats, 
        'another_member': another_member,
        'room_id': room_name,
        'username': request.user.username,
        'friends_list': Friend.objects.get(student__user__user=request.user),
    })

@login_required
def create_room(request):
    if request.method == "POST":
        add_user_valid = get_user_contact(request.POST["create_room_username"])
        loggedin_user = request.user

        if str(loggedin_user) != add_user_valid:
            try:
                already_exists = Room.objects.filter(room_type = False).filter(members__username = loggedin_user).filter(members__username = request.POST["create_room_username"]).get()
                return redirect("chat:room", already_exists)
            except Room.DoesNotExist:
                current_user_valid = get_user_contact(loggedin_user)
                if Friend.objects.filter(student=current_user_valid).exists():
                    studObject = Friend.objects.get(student=current_user_valid)
                    studObject.friends.add(add_user_valid)
                    studObject.save()
                else:
                    new_friend = Friend.objects.create(
                        student=current_user_valid
                    )
                    new_friend.friends.add(add_user_valid)
                    new_friend.save()
                if Friend.objects.filter(student=add_user_valid).exists():
                    studObject1 = Friend.objects.get(student=add_user_valid)
                    studObject1.friends.add(current_user_valid)
                    studObject1.save()
                else:
                    new_friend_repeat = Friend.objects.create(
                        student=add_user_valid
                    )
                    new_friend_repeat.friends.add(current_user_valid)
                    new_friend_repeat.save()
                new_room = Room.objects.create()
                new_room.members.add(get_object_or_404(User, username=request.POST["create_room_username"]))
                new_room.save()
                new_room.members.add(request.user)
                new_room.save()
                previousNotifId = request.POST.get('notfiid', None)
                if previousNotifId:
                    previousNotifi = get_object_or_404(Notification, pk=previousNotifId)
                    previousNotifi.viewed = True
                    previousNotifi.save()
                    messReq = get_object_or_404(MessageRequest, pk=previousNotifi.identifier)
                    messReq.status = True
                    messReq.save()
                    notfi = Notification.objects.create(
                        fromUser=request.user,
                        toUser=add_user_valid.user.user,
                        notificationType='acceptFriendRequest',
                        content='New Friend Request Accepted',
                        identifier=new_room.pk
                    )
                return redirect('chat:room', new_room.pk)
    return HttpResponse('<html><body> Some error in post request of create room .</body></html>') 

@login_required
def landlord_chat(request, slug):
    property_details = get_object_or_404(Property, urlSlug=slug)
    property_landlord_valid = get_object_or_404(User, username=property_details.landlord.user.user.username)
    loggedin_user = request.user
    try:
        already_exists = Room.objects.filter(room_type = False).filter(members__username = loggedin_user).filter(members__username = property_landlord_valid).get()
        notfi = Notification.objects.create(
                    fromUser=request.user,
                    toUser=property_landlord_valid,
                    notificationType='newChatLandlord',
                    content=property_details.title,
                    identifier=already_exists.pk,
                )
        return redirect("chat:room", already_exists)
    except Room.DoesNotExist:
        new_room = Room.objects.create()
        new_room.members.add(get_object_or_404(User, username=property_landlord_valid))
        new_room.save()
        new_room.members.add(request.user)
        new_room.save()
        notfi = Notification.objects.create(
                    fromUser=request.user,
                    toUser=property_landlord_valid,
                    notificationType='newChatLandlord',
                    content=property_details.title,
                    identifier=new_room.pk,
                )
        return redirect('chat:room', new_room.pk)
    

@method_decorator(login_required, name='dispatch')
class RequestView(ListView):
    context_object_name = 'message_request_list'
    template_name = "chat/message_list.html"
    def get_queryset(self):
        return MessageRequest.objects.filter(request_sender__user__user=self.request.user)


@login_required
def message_request_update(request):  
    if request.method == "GET":
        return render(request, 'chat/message_request.html')

    if request.method == "POST":
        new_request_user_name = request.POST["new_chat_request_name"]
        add_user_valid = get_user_contact(new_request_user_name)

        loggedin_user = request.user

        if loggedin_user.username != request.POST["new_chat_request_name"]:
            try:
                already_exists = MessageRequest.objects.filter(request_sender__user=add_user_valid.user).get()
                print("Message request sent to this user ==> ", already_exists)
                return HttpResponse('<html><body>Request sent already %s.</body></html>' % already_exists)
            except MessageRequest.DoesNotExist:
                new_message_request = MessageRequest.objects.create(
                        logged_in_user = get_user_contact(loggedin_user),
                        request_sender = get_user_contact(new_request_user_name)
                )
                notfi = Notification.objects.create(
                    fromUser=loggedin_user,
                    toUser=get_object_or_404(User, username=new_request_user_name),
                    notificationType='newFriendRequest',
                    content=new_message_request.logged_in_user,
                    identifier=new_message_request.pk
                )
                return HttpResponse('<html><body>Request sent sucessfully.</body></html>')

    return redirect('chat:index')


@method_decorator(login_required, name='dispatch')
class CreateGroupView(ListView):
    context_object_name = 'friends_list'
    template_name = "chat/roommates_groups.html"
    def get_queryset(self):
        fav = Friend.objects.filter(student__user__user=self.request.user)
        # print(fav[0].to_friend)
        return Friend.objects.filter(student__user__user=self.request.user)
    
    @staticmethod
    def post(request):
        group_members_list = request.POST.getlist('group_members_list')
        new_room = Room.objects.create(name = request.POST['groupname'], room_type=True)
        new_room.save()
        for each_member in group_members_list:
            add_member_valid = get_object_or_404(User, username=each_member)
            new_room.members.add(add_member_valid)
        new_room.save()
        new_room.members.add(request.user)
        new_room.save()
        return redirect('chat:group', new_room.pk)