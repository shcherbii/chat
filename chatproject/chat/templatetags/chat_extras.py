from django import template
from django.contrib.auth import get_user_model
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from chat.models import UserPrivareChatRequest, Chat, UserChatNotification
from django.contrib.auth.models import User
import logging


register = template.Library()
user_model = get_user_model()


@register.inclusion_tag("chat/notifications.html")
def user_chat_requests(chat_id):
    chat = User.objects.get(chat_id = chat_id)

    users_requests = UserPrivareChatRequest.objects.filter(chat = chat, request_status = 2)

    return {"users_requests": users_requests}


@register.inclusion_tag("chat/rooms_list.html")
def chat_rooms(user, request=False):
    search_chat = request.GET.get('search_chat')

    if search_chat:
        chats = Chat.objects.filter(name__icontains = search_chat, type__type = 'group')[:10]
        rooms_notification = UserChatNotification.objects.filter(user = user)
        users = User.objects.filter(username__icontains = search_chat).exclude(username = user)[:10]

        return {'group_chat': chats, 'personal_chat':None, 'user':user, 'rooms_notification':rooms_notification, 'findusers':users}
    else:
        user = User.objects.get(username = user)
        rooms_notification = UserChatNotification.objects.filter(user = user)
        # if chat_user.chat.type.id == 1
        group_chat = [chat_user.chat for chat_user in user.chatusers_set.all() if chat_user.chat.type.type == 'group' and chat_user.status == 'active' ]
        personal_chat = [chat_user.chat for chat_user in user.chatusers_set.all() if chat_user.chat.type.type == 'personal' and chat_user.status == 'active']
        
        return {'group_chat': group_chat, 'personal_chat':personal_chat, 'user':user, 'rooms_notification':rooms_notification, 'findusers':None}