from django.urls import path
from .views import (
    CourseView,
    CourseDetailView,
    studentsCourseView,
    studentsCourseDetailView,
)

urlpatterns = [
    path(
        "courses/",
        CourseView.as_view(),
    ),
    path("courses/<uuid:course_id>/", CourseDetailView.as_view()),
    path("courses/<uuid:course_id>/students/", studentsCourseView.as_view()),
    path(
        "courses/<uuid:course_id>/students/<uuid:student_id>/",
        studentsCourseDetailView.as_view(),
    ),
]
