from rest_framework import serializers
from students_courses.models import StudentCourse


class StudentCourseSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    student_email = serializers.CharField(source="student.email")

    class Meta:
        model = StudentCourse
        fields = [
            "id",
            "status",
            "student_id",
            # "course",
            "student_username",
            "student_email",
        ]
