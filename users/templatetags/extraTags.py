from django import template
from django.urls import reverse
from notifications.models import Notification
from chat.models import Room, MessageRequest
import phonenumbers

register = template.Library()

@register.filter(name="phonenumber")
def phonenumberFormat(value):
    return "+1 {}".format(phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.NATIONAL))

# Need to enable when we use interest as filters in roommate post

# @register.filter(name="filterurl")
# def filterCorrectUrl(value, currentfilter):
#     if currentfilter:
#         currentfilter = currentfilter.replace('.', '')
#         currentfilter = list(currentfilter)
#         for i in currentfilter:
#             if i == str(value):
#                 currentfilter.remove(i)
#                 return '.'.join(currentfilter)

#         url = "{}.{}".format('.'.join(currentfilter), value)
#         return url
#     else:
#         return value

# @register.filter(name="filterclass")
# def filterClass(value, currentfilter):
#     if currentfilter:
#         currentfilter = currentfilter.replace('.', '')
#         currentfilter = list(currentfilter)
#         for i in currentfilter:
#             if i == str(value):
#                 return True
#         return False
#     else:
#         return False

@register.filter(name="checkboxActive")
def checkboxActive(value):
    if value.data.get('selected', False):
        return True
    return False

@register.simple_tag(takes_context=True)
def get_all_notifications(context):
    user = context.get("user")
    if user.is_authenticated:
        notifi = Notification.objects.filter(toUser=user, viewed=False)
        return notifi

@register.simple_tag(takes_context=True)
def get_invite_url(context):
    user = context.get("user")
    try:
        code = user.usertype.userstudent.student_invite.inviteCode
    except:
        code=None
    if user.is_authenticated:
        if code:
            url = context.get("request").build_absolute_uri(reverse('user:home'))
            url_full = '{}{}{}'.format(url, "?invite_code=", code)
            return url_full
        else:
            return 'Save the profile to generete invite code.'

@register.simple_tag(takes_context=True)
def get_friend_status(context, postAuthor):
    user = context.get("user")
    if user.is_authenticated:
        try:
            if user.usertype.userstudent.friend.friends.filter(user=postAuthor.user).exists():
                room = Room.objects.filter(room_type=False).filter(members=user).filter(members=postAuthor.user.user).first()
                return {'status': 'Friends', 'url': room.pk}
        except:
            pass
        messageRequests = MessageRequest.objects.filter(logged_in_user=user.usertype.userstudent).filter(request_sender=postAuthor).filter(status=False)
        if messageRequests:
            return {'status': 'FriendRequestSent'}
        return {'status': 'NotFriends'}