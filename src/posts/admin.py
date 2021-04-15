"""Post models admin."""

# Django
from django.contrib import admin

#Models
from src.posts.models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    exclude = ("image", "content_type")


# Register the admin class with the associated model
admin.site.register(Post, PostAdmin)


admin.site.register(Tag)
