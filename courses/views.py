from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from accounts.models import Account
from .models import Course


from .serializers import (
    CourseSerializer,
    CourseRetrieveUpdateDestroySerializer,
    studentsAssociatedWithTheCourse,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrReadOnly, IsRegisteredAccount, IsAdmin


class CourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsRegisteredAccount]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsRegisteredAccount]
    queryset = Course.objects.all()
    serializer_class = CourseRetrieveUpdateDestroySerializer
    lookup_url_kwarg = "course_id"
    http_method_names = ["get", "patch", "delete"]


class studentsCourseView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    queryset = Course.objects.all()
    serializer_class = studentsAssociatedWithTheCourse
    lookup_url_kwarg = "course_id"
    http_method_names = ["put", "get"]


class studentsCourseDetailView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    def perform_destroy(self, instance):
        student = get_object_or_404(Account, pk=self.kwargs["student_id"])

        course_students = instance.students.all()

        if student not in course_students:
            raise NotFound({"detail": "this id is not associated with this course."})
        else:
            instance.students.remove(student)
