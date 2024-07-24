from rest_framework import permissions


class IsAdminAuthorModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.method == 'POST' and request.user.is_authenticated)
            or (request.method == 'PATCH' and request.user.is_authenticated)
            or (request.method == 'PUT' and request.user.is_authenticated)
            or (request.method == 'DELETE' and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.method == 'PATCH'
                and (request.user.role == 'moderator'
                     or request.user.role == 'admin'
                     or obj.author == request.user))
            or (request.method == 'DELETE'
                and (request.user.role == 'moderator'
                     or request.user.role == 'admin'
                     or obj.author == request.user))
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.role == 'admin')
        )


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
