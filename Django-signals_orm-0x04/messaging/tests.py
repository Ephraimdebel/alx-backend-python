# messaging/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="pass123")
        self.receiver = User.objects.create_user(username="receiver", password="pass123")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello!"
        )
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)
        n = notifications.first()
        self.assertEqual(n.message, msg)
        self.assertFalse(n.is_read)

    def test_no_notification_when_sender_equals_receiver(self):
        # Optional: verify we do not create notification if sender == receiver
        msg = Message.objects.create(sender=self.sender, receiver=self.sender, content="Hey me")
        notifications = Notification.objects.filter(message=msg)
        self.assertEqual(notifications.count(), 0)
