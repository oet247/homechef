from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("home", views.home),
    path("login", views.login_test),
    path("logout", views.logout_test),
]