from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff
        )


class IsAdminModerOrAuthor(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )


class IsAdminOrSuperUserReadOnly(IsAdminOrSuperUser):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )
