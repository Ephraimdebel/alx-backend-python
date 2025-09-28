from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for participants
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()

        # Restrict PUT, PATCH, DELETE to participants only
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()

        return False
