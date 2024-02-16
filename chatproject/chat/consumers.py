from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Chat, ChatMassages, UserChatNotification, ChatUsers
from itertools import chain


class ChatConsumer(AsyncWebsocketConsumer):

    room_users = {}

    async def connect(self):    
        user = self.scope['user']
       
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat{self.chat_id}'

        key, value = self.chat_id, user

        try:
            self.room_users[key].add(value)
        except KeyError:
            self.room_users[key] = {value}

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):

        key, value = self.chat_id, self.scope['user']
        try:
            self.room_users[key].remove(value)
        except KeyError:
            pass

        await self.channel_layer.group_discard(
            self.channel_layer,
            self.room_group_name
        )

    async def receive(self,text_data):
        data = json.loads(text_data)
        # print(self.room_users[self.chat_id])
        message = data['message']
        username = data['username']
        room = data['room']

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':message,
                'username':username,
                'room':room,
            }
        )

        await self.save_massage(username, room, message)
        await self.save_notification(room, self.room_users[self.chat_id])

    async def chat_message(self, event):
        print('send')
        message = event['message']
        username = event['username']
        room = event['room']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'room':room,
        }))

    @sync_to_async
    def save_massage(self, username, room, message):
        user = User.objects.get(username=username)
        room = Chat.objects.get(chat_id=room)
        ChatMassages.objects.create(user=user, chat=room, massage_content = message)

    @sync_to_async
    def save_notification(self, room, room_users):
        room = Chat.objects.get(chat_id=room)
        room_user = ChatUsers.objects.filter(chat = room)
        users = [chat_user.user for chat_user in room_user]
        for user in users:
            if user in room_users:
                pass
            else:
                notificate, created = UserChatNotification.objects.get_or_create(user=user, chat = room)
                if created == False:
                    notificate.count_massages += 1
                    notificate.save()
        
        # if room.creator in room_users:
        #     pass
        # else:
        #     notificate, created = UserChatNotification.objects.get_or_create(user=room.creator, room = room)
        #     if created == False:
        #         notificate.count_massages += 1
        #         notificate.save()
    

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        self.group_name = f'global_{user.username}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    
    async def send_notification(self, event):
        
        user = event['massages_user']
        room = event['massages_room']

        await self.send(text_data=json.dumps({ 'count_massages': event['count_massages'], 'massages_user': user.username, 'massages_room': room.chat_id}))