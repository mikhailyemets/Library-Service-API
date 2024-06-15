from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_staff)
            or (request.user is not None)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            (request.user and request.user.is_staff)
            or (obj.user == request.user)
        )
