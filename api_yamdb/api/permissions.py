from rest_framework import permissions

from custom_user.models import CustomUser


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            request.user.is_authenticated
            and request.user.role == CustomUser.Roles.admin
        )


class IsAdminModerOrAuthorOrPostNew(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            view.action == 'create'
            or request.user.is_superuser
            or request.user.role == CustomUser.Roles.admin
            or request.user.role == CustomUser.Roles.moderator
            or request.user == obj.author
        )


class GenreCategoryPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ['create', 'destroy']:
            return request.user.is_authenticated and request.user.is_superuser or (
                request.user.is_authenticated
                and request.user.role == CustomUser.Roles.admin
            )
