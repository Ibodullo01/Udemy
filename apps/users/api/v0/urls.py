from django.urls import path
from .views import register, login, log_out, update_profile

app_name = 'users'

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", log_out, name="logout"),
    path("update_profile/", update_profile, name="update_profile"),

]

