from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterUserView, LogoutUserView, LoginUserView

app_name = "authuser"

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
]
