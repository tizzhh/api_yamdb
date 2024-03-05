from rest_framework import permissions

from custom_user.models import CustomUser


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            not request.user.is_anonymous
            and request.user.role == CustomUser.Roles.admin
        )
