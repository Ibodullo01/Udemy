from django.urls import path
from .views import (course_create, course_list, course_detail,
                    lesson_create, card_create, card_list, card_remove,
                    favorite_courses, favorite_list_view, purchase_course ,
                    purchase_course_list, delete_purchase_course,
                    course_comment_create_view,lesson_comment_create_view, course_cooment_list, lesson_comment_list)

app_name = "courses_api"

urlpatterns = [
    path('create/', course_create, name='course-create'),
    path('course_list/', course_list, name='course-list'),
    path('course_detail/<int:pk>/', course_detail, name='course-detail'),
    path('lesson/create/', lesson_create, name='lesson-create'),
    path('card/create/', card_create, name='card-create'),
    path('card/list/', card_list, name='card-list'),
    path('card/remove/<int:pk>/', card_remove, name='card-remove'),
    path('courses/favorite/', favorite_courses, name='favorite-courses'),
    path('favorite_list/', favorite_list_view, name='favorite-list'),
    path('courses/purchase/', purchase_course, name='purchase-course'),
    path('my-courses/', purchase_course_list, name='purchase-list'),
    path('my-courses/delete/<int:pk>/', delete_purchase_course, name='purchase-course'),
    path('course_comment/create/', course_comment_create_view, name='course-comment-create'),
    path('lesson_comment/create/', lesson_comment_create_view, name='lesson-comment-create'),
    path('course_comment_list/<int:pk>/', course_cooment_list, name='course-comment-list'),
    path('lesson_comment_list/<int:pk>/', lesson_comment_list , name='lesson-comment-list'),




]
