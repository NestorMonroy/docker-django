from django.urls import path, reverse_lazy
from src.posts.views import posts as post_views

app_name = "posts"

urlpatterns = [
    path("", post_views.PostListView.as_view(), name="all"),
    path("post/<slug:slug>/", post_views.PostDetailView.as_view(), name="post_detail"),
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
    path(
        "post/<slug:slug>/comment",
        post_views.CommentCreateView.as_view(),
        name="post_comment_create",
    ),
    path(
        "comment/<int:pk>/delete",
        post_views.CommentDeleteView.as_view(success_url=reverse_lazy("posts")),
        name="post_comment_delete",
    ),
]
