from django.urls import path
from .views import academic_year_list_view

app_name = "kadr_api"

urlpatterns = [
    path('academic_years/', academic_year_list_view, name='academic_year_list'),
]
