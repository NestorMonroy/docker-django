from django.urls import path, reverse_lazy
from src.posts.views import posts as post_views

app_name = "posts"

urlpatterns = [
    path("", post_views.PostListView.as_view(), name="all"),
    path(
        "post/create",
        post_views.PostCreateView.as_view(),
        name="post_create",
    ),
]
