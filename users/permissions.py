from rest_framework import permissions
from django.contrib.auth.models import User
from typing import cast


class IsStaffOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff or admins to edit objects.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to staff or admin
        if not (request.user and request.user.is_authenticated):
            return False

        user = cast(User, request.user)

        if user.is_staff or user.is_superuser:
            return True

        # Check for profile role
        profile = getattr(user, "profile", None)
        if profile and profile.role in ["staff", "admin"]:
            return True

        return False


class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        user = cast(User, request.user)

        if user.is_superuser:
            return True

        profile = getattr(user, "profile", None)
        if profile and profile.role == "admin":
            return True

        return False
