from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

"""@receiver(post_save, sender=Message)
def send_chat_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        sender_user = instance.user
        receiver_user = instance.receiver
        message_content = instance.content

        async_to_sync(channel_layer.group_send)(
            f'user_{receiver_user.id}',
            {
                'type': 'chat_message',
                'message': {
                    'sender': sender_user.username,
                    'content': message_content,
                }
            }
        )"""