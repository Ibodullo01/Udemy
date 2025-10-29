from rest_framework import serializers
from apps.kadr.models import AcademicYear, Course, Direction, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'file', 'creation_date']


class DirectionSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Direction
        fields = ['id', 'title', 'creation_date', 'subjects']


class CourseSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'creation_date', 'directions']


class AcademicYearSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'creation_date', 'courses']
