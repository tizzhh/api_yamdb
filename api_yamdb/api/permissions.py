from rest_framework import permissions

from custom_user.models import CustomUser


class IsAdminOrSuperUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            request.user.is_authenticated
            and request.user.role == CustomUser.Roles.admin
        )


class IsAnyAuth(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            any(
                request.user.role == role[0]
                for role in CustomUser.Roles.choices
            )
            or request.user.is_superuser
        )
