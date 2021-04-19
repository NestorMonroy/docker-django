from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from src.users.views import users as users_views

app_name = "users"

urlpatterns = [
    path("signup/", users_views.SingupView.as_view(), name="signup"),
    path("login/", users_views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    re_path(
        r"^email/confirm/(?P<key>[0-9A-Za-z]+)/$",
        users_views.AccountEmailActivateView.as_view(),
        name="email-activate",
    ),
    re_path(
        r"^email/resend-activation/$",
        users_views.AccountEmailActivateView.as_view(),
        name="resend-activation",
    ),
]
