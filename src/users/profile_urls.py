from django.urls import path

from src.users.views import profiles as profile_views

app_name = "profile"

urlpatterns = [
    path("", profile_views.ProfileHomeView.as_view(), name="home"),
    path(
        "details/", profile_views.profile_detail_update, name="user-update"
    ),
]
