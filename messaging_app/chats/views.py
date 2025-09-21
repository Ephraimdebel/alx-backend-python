# messaging_app/chats/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

# Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    # Endpoint to create a new conversation
    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get("participants", [])
        if not participants_ids:
            return Response(
                {"error": "Participants are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        conversation = Conversation.objects.create()
        conversation.participants.set(participants_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer

    # Endpoint to send a new message
    def create(self, request, *args, **kwargs):
        sender_id = request.data.get("sender")
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not all([sender_id, conversation_id, message_body]):
            return Response(
                {"error": "sender, conversation, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(
            sender_id=sender_id,
            conversation_id=conversation_id,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
