from django.shortcuts import render, get_object_or_404, redirect

from .models import Notification
from chat.models import Room, MessageRequest
# Create your views here.

def notification(request, pk):
    obj = get_object_or_404(Notification, pk=pk)

    if obj.notificationType == 'rentRequest':
        obj.viewed = True
        obj.save()
        return redirect('checkout:rentRequestDetail', pk=obj.identifier)

    if obj.notificationType == 'tourRequest':
        obj.viewed = True
        obj.save()
        return redirect('checkout:tourRequestDetail', pk=obj.identifier)

    if obj.notificationType == 'question' or obj.notificationType == 'answered':
        obj.viewed = True
        obj.save()
        return redirect('property:propertyDetail', slug=obj.identifier)

    if obj.notificationType == 'serviceRequest':
        obj.viewed = True
        obj.save()
        return redirect('services:servicesDetail', pk=obj.identifier)
    
    if obj.notificationType == 'deletedQuestion' or obj.notificationType == 'tagFriend':
        obj.viewed = True
        obj.save()
        return redirect('property:propertyDetail', slug=obj.identifier)
    
    if obj.notificationType == 'newChatLandlord' or obj.notificationType == 'newMessage' or obj.notificationType == 'acceptFriendRequest':
        obj.viewed = True
        obj.save()
        room = get_object_or_404(Room, pk=obj.identifier)
        if room.room_type:
            return redirect('chat:group', room_name=obj.identifier)
        else:
            return redirect('chat:room', room_name=obj.identifier)
        
    if obj.notificationType == 'newFriendRequest':
        obj.viewed = True
        obj.save()
        messReqObj = get_object_or_404(MessageRequest, pk=obj.identifier)
        messReqObj.delete()
        notif = Notification.objects.create(
                    fromUser=request.user,
                    toUser=obj.fromUser,
                    notificationType='denyFriendRequest',
                    content='Friend Request Denied',
                    identifier='Friend Request Denied',
                )
        return redirect('chat:index')
    if obj.notificationType == 'denyFriendRequest':
        obj.viewed = True
        obj.save()
        return redirect('chat:index')
