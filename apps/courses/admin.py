from PIL.JpegImagePlugin import jpeg_factory
from django.contrib import admin

from apps.courses.models import Lesson, Course, LessonComment, CourseComment, Cart, PurchasedCourse

# Register your models here.

admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(LessonComment)
admin.site.register(CourseComment)
admin.site.register(Cart)
admin.site.register(PurchasedCourse)

