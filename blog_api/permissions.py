# blog_api/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read allowed for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # write only for owner
        return obj.author == request.user
