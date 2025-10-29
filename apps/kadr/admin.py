from django.contrib import admin
from apps.kadr.models import Direction, AcademicYear, Course, Subject


# Inline: Course -> Academic_year
class CourseInline(admin.TabularInline):
    model = Course
    extra = 1


# Inline: Direction -> Course
class DirectionInline(admin.TabularInline):
    model = Direction
    extra = 1


# Inline: Subject -> Direction
class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


# ModelAdmin sozlamalari
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'creation_date')
    inlines = [CourseInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'academic_year', 'creation_date')
    inlines = [DirectionInline]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'creation_date')
    inlines = [SubjectInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'direction', 'file', 'creation_date')