from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Save old content before updating a message"""
    if instance.pk:  # means it's an update, not a new message
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:  # content is changing
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.edited = True  # mark as edited
        except Message.DoesNotExist:
            pass