# messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    Create a Notification for the receiver when a new Message is created.
    Avoid creating a notification if the sender == receiver (optional).
    """
    if not created:
        return

    # Avoid notifying when user messages themselves (optional behaviour)
    if instance.sender == instance.receiver:
        return

    Notification.objects.create(user=instance.receiver, message=instance)
