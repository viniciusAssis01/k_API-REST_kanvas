from rest_framework import permissions
from rest_framework.views import View, Request
from .models import Content


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class isYourCourseContentOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Content):
        return (
            request.user.is_superuser
            or request.user in obj.course.students.all()
            and request.method in permissions.SAFE_METHODS
        )
