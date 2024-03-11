from rest_framework import permissions

from yamdb_user.models import YamdbUser


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            request.user.is_authenticated
            and request.user.role == YamdbUser.Roles.admin
        )


class IsAdminModerOrAuthorOrPostNew(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                view.action == 'create'
                or request.user.is_superuser
                or request.user.role == YamdbUser.Roles.admin
                or request.user.role == YamdbUser.Roles.moderator
                or request.user == obj.author
            )
        )
