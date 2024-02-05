from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# Create your models here.

class RoomType(models.Model):
    
    type = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.type

class ChatRoom(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(RoomType, default = 2, on_delete=models.CASCADE)
    uniqe_key = models.CharField(max_length=100, unique=True)
    room_user = models.ManyToManyField(User, related_name='room_users', blank=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *arg, **kwargs):
 
        if not self.uniqe_key:
            unique_id = uuid.uuid4()
            self.uniqe_key = unique_id


        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*arg, **kwargs)
    
class ChatMassages(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    massage_content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('date', )

    def __str__(self) -> str:
        return self.user.username + ' send in room: ' + self.room.name


class UserPrivareRoomRequest(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    request_status = models.IntegerField(default = 2)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.username + ' send request to join a room: ' + self.room.name