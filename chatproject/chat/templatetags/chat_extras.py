from django import template
from django.contrib.auth import get_user_model
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from chat.models import UserPrivareRoomRequest
import logging


register = template.Library()
user_model = get_user_model()


@register.inclusion_tag("chat/notifications.html")
def recent_posts(current_user):
    users_requests = UserPrivareRoomRequest.objects.filter(room__creator = current_user, request_status =2)

    return {"users_requests": users_requests}