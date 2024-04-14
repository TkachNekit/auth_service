from django.urls import path
from rest_framework import routers

from users.views import RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView

app_name = 'users'

router = routers.DefaultRouter()

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("me/", UserAPIView.as_view()),
    path("refresh/", RefreshAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
]
