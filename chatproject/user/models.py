from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    decs = models.TextField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='users/2024/02/09/images.png', blank=True)

    def __str__(self) -> str:
        return self.user.username