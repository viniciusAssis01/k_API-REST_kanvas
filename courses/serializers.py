from accounts.models import Account
from .models import Course
from rest_framework import serializers
from students_courses.serializers import (
    StudentCourseSerializer,
)
from contents.serializers import ContentSerializer
from accounts.serializers import AccountSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        ]
        extra_kwargs = {
            "contents": {"read_only": True},
            "students_courses": {"read_only": True},
        }


class CourseRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(read_only=True, many=True)
    contents = ContentSerializer(read_only=True, many=True)
    instructor = AccountSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        ]


class studentsAssociatedWithTheCourse(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "name", "students_courses"]
        extra_kwargs = {"name": {"read_only": True}}

    def update(self, instance: Course, validated_data: dict) -> Course:
        students = []
        email_notFound = []
        for student_in_course in validated_data["students_courses"]:
            student = student_in_course["student"]
            student_found = Account.objects.filter(email=student["email"]).first()

            if not student_found:
                email_notFound.append(student["email"])
            else:
                students.append(student_found)

        if email_notFound:
            raise serializers.ValidationError(
                {
                    "detail": f'No active accounts was found: {", ".join(email_notFound)}.'
                }
            )

        if not self.partial:
            instance.students.add(*students)
            return instance

        return super().update(instance, validated_data)
