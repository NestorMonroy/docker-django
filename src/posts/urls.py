from django.urls import path, reverse_lazy
from src.posts.views import posts as post_views

app_name = "posts"

urlpatterns = [
    path("", post_views.PostListView.as_view(), name="all"),
    path("post/<slug:slug>/", post_views.PostDetailView.as_view(), name="detail"),
    path(
        "post/create",
        post_views.PostCreateView.as_view(),
        name="create",
    ),
    path(
        "post/<slug:slug>/update",
        post_views.PostUpdateView.as_view(),
        name="post_update",
    ),
    path(
        "post/<slug:slug>/delete",
        post_views.PostDeleteView.as_view(),
        name="post_delete",
    ),
    path("post_picture/<slug:slug>", post_views.stream_file, name="post_picture"),
]
