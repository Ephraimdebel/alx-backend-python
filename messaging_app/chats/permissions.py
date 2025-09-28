from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own messages
    and conversations.
    """

    def has_object_permission(self, request, view, obj):
        # For example, if your Message model has a 'sender' field
        # and Conversation model has a 'user' or 'participants' field
        return getattr(obj, "sender", None) == request.user or \
               getattr(obj, "user", None) == request.user or \
               request.user in getattr(obj, "participants", [])
