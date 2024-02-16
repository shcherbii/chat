from django.contrib import admin
from .models import Chat, ChatMassages, ChatType, UserPrivareChatRequest, UserChatNotification, ChatUsers, ChatUserType
# Register your models here.

admin.site.register(Chat)
admin.site.register(ChatMassages)
admin.site.register(ChatUsers)
admin.site.register(ChatUserType)
admin.site.register(ChatType)
admin.site.register(UserPrivareChatRequest)
admin.site.register(UserChatNotification)




