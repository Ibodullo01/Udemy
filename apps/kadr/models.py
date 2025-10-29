from django.db import models
from django.db import models

class AcademicYear(models.Model):
    year = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.year)


class Course(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Direction(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='directions')
    title = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subject(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='subjects')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='subjects/')
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
