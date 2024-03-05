from rest_framework import permissions

from custom_user.models import CustomUser


class IsAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.role == CustomUser.Roles.admin
