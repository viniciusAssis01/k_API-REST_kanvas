from rest_framework import permissions
from rest_framework.views import View, Request
from .models import Course


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated
            or request.user.is_authenticated
            and request.user.is_superuser
        )


class IsRegisteredAccount(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.user.is_superuser:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request: Request, view: View, obj: Course):
        return request.user.is_superuser or request.user in obj.students.all()


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
