from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class ChatType(models.Model):
    
    type = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.type

class ChatUserType(models.Model):
    
    type = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.type

class Chat(models.Model):

    name = models.CharField(max_length=100)
    type = models.ForeignKey(ChatType, default = 1, on_delete=models.SET_DEFAULT)
    chat_id = models.CharField(max_length=39, unique=True, null=True)
    is_private = models.BooleanField(default = True)
    photo = models.ImageField(upload_to='chats/%Y/%m/%d', blank=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *arg, **kwargs):
        if not self.chat_id:
            unique_id = uuid.uuid4()
            self.chat_id = unique_id.int

        super().save(*arg, **kwargs)
    
class ChatUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    type = models.ForeignKey(ChatUserType, default = 1, on_delete=models.SET_DEFAULT)
    status = models.CharField(max_length = 20, default = 'active')


class ChatMassages(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    type = models.CharField(default = 'users')
    massage_content = models.TextField()

    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('date', )

    def __str__(self) -> str:
        if self.user:
            return self.user.username + ' send in Chat: ' + self.chat.name
        else:
            return 'System send in Chat: ' + self.chat.name



class UserPrivareChatRequest(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    request_status = models.IntegerField(default = 2)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.username + ' send request to join a Chat: ' + self.chat.name
    

class UserChatNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    count_massages = models.IntegerField(default = 1)

    def __str__(self) -> str:
        return self.user.username + ' recive notification in Chat: ' + self.chat.name