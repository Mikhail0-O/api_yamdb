from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or obj.author == request.user
            or request.user.is_staff or request.user.is_superuser
        )
