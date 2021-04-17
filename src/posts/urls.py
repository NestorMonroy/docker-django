from django.urls import path, reverse_lazy
from src.posts.views import posts as post_views
from src.posts.views import tags as tags_views

app_name = "posts"

urlpatterns = [
    path("", post_views.post_list, name="all"),
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
    path(
        "post/<int:pk>/favorite",
        post_views.AddFavoriteView.as_view(),
        name="post_favorite",
    ),
    path(
        "post/<int:pk>/unfavorite",
        post_views.DeleteFavoriteView.as_view(),
        name="post_unfavorite",
    ),
    path(
        "tag/<slug:slug>/",
        tags_views.search_tag,
        name="tag_list",
    ),
    path(
        "tag_list_create/",
        tags_views.TagListView.as_view(),
        name="tag_list_create",
    ),
    path("tag-creation/", tags_views.tag_creation_view, name="tag_create"),
    path(
        "tag-edit-or-update/<int:pk>/<slug:action>/",
        tags_views.update_or_delete_tag_view,
        name="tag_edit_or_update",
    ),
    path(
        "ajax-update/tag/<int:pk>/",
        tags_views.ajax_update_tag_view,
        name="ajax_update_tag",
    ),
]
