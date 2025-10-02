from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return unread messages for the given user.
        Optimized with .only() to load only necessary fields.
        """
        return self.filter(receiver=user, read=False).only("id", "sender", "content", "timestamp")
