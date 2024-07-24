from django.conf import settings

from rest_framework import permissions


class IsAdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('PATCH', 'DELETE'):
            return (
                    request.user.role in (settings.ROLE_MODERATOR,
                                          settings.ROLE_ADMIN)
                    or obj.author == request.user
            )
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == settings.ROLE_ADMIN)
        )


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
