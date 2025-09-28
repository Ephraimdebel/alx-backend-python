from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversations
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # For Messages
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
