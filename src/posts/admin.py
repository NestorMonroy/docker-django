"""Post models admin."""

# Django
from django.contrib import admin

# Models
from src.posts.models import Post


admin.site.register(Post)
