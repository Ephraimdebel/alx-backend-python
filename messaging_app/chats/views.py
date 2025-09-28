from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name"]

    def get_queryset(self):
        # Only show conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user).prefetch_related("participants", "messages")

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Ensure the creator is a participant
        conversation.participants.add(self.request.user)
        return conversation


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]

    def get_queryset(self):
        # Filter messages only from conversations where the user is a participant
        conversation_id = self.request.query_params.get("conversation_id")
        if conversation_id:
            return Message.objects.filter(conversation__id=conversation_id, conversation__participants=self.request.user).select_related("sender", "conversation")
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to send messages in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
