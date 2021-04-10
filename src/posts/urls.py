from django.urls import path, reverse_lazy
from src.posts.views import posts as post_views

app_name = "posts"

urlpatterns = [
    path("", post_views.PostListView.as_view(), name="all"),
    path(
        "post/create",
        post_views.PostCreateView.as_view(success_url=reverse_lazy("posts:all")),
        name="post_create",
    ),
]
