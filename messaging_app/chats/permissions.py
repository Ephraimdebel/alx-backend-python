from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to send, view, update, and delete messages.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is authenticated and is part of the conversation.
        Assumes:
          - Message model has a `conversation` foreign key
          - Conversation model has a `participants` ManyToManyField
        """
        if not request.user or not request.user.is_authenticated:
            return False

        conversation = getattr(obj, "conversation", None)
        if conversation is None:
            return False

        return request.user in conversation.participants.all()
