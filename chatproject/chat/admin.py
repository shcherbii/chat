from django.contrib import admin
from .models import ChatRoom, ChatMassages, RoomType, UserPrivareRoomRequest
# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(ChatMassages)
admin.site.register(RoomType)
admin.site.register(UserPrivareRoomRequest)
