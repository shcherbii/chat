from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import UserChatNotification

@receiver(post_save, sender=UserChatNotification)
def notification_created(sender, instance, created, **kwargs):

    # if created:
    #     print(instance.user.username)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'global_{instance.user.username}',
        {
            "type": "send_notification",
            "massages_user": instance.user,
            "massages_room": instance.chat,
            "count_massages": instance.count_massages
        }
    )