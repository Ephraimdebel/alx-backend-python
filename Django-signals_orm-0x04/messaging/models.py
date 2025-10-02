from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for the given user.
        Uses .only() to optimize by loading only needed fields.
        """
        return self.filter(receiver=user, read=False).only("id", "sender", "content", "timestamp")
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # REQUIRED FIELD
    read = models.BooleanField(default=False)  # ✅ new field

    # Default manager
    objects = models.Manager()
    # Custom unread manager
    unread = UnreadMessagesManager()
    parent_message = models.ForeignKey(
            "self",
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            related_name="replies"
        )

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # <-- Who edited it
    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"