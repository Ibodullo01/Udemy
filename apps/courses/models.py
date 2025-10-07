from django.db import models
from apps.users.models import User


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField(default=0)
    description = models.TextField()
    full_description = models.TextField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, default="Beginner")
    category = models.CharField(max_length=100, default="General")
    lessons_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    lesson_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    duration = models.CharField(max_length=100)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['lesson_number']


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"

    class Meta:
        ordering = ['-date']
