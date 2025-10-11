from django.utils import timezone

from PIL.JpegImagePlugin import jpeg_factory
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
    card_image = models.ImageField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, default="Beginner")
    category = models.CharField(max_length=100, default="General")
    lessons_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['lesson_number']



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_courses')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'course')  # bir foydalanuvchi bir kursni 2 marta saqlay olmasin

    def __str__(self):
        return f"{self.user.fullname} → {self.course.title}"

class CourseComment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_comments')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.fullname} -> {self.course.title}"

class LessonComment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_comments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_comments')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.fullname} -> {self.lesson.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.fullname} → {self.course.title}"

class PurchasedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='purchased_by')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

