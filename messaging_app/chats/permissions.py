# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to allow users to access only their own objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
