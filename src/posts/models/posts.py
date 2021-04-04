"""Posts model."""
# Django
from django.db import models

# Utilities
from src.utils.models import TeamGralModel

STATUS = ((0, "Draft"), (1, "Publish"))

from src.utils.extra import upload_post_image_path


class Post(TeamGralModel):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to=upload_post_image_path, blank=True, null=True)
    other = models.CharField(blank=True, null=True, max_length=100)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at", "-updated_at"]