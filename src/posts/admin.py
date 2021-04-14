"""Post models admin."""

# Django
from django.contrib import admin

# Models
from src.posts.models import Post, Tag


admin.site.register(Tag)
admin.site.register(Post)
