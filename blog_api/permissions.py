# blog_api/permissions.py
from rest_framework import permissions, SAFE_METHODS

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    SAFE_METHODS (GET/HEAD/OPTIONS) sabko allow.
    Write methods only to object owner.
    """
    def has_object_permission(self, request, view, obj):
        # read allowed for all
        if request.method in SAFE_METHODS:
            return True
        # write only for owner
        return hasattr(obj, 'author') and obj.author == request.user
