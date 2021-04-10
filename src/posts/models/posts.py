"""Posts model."""
# Django
from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

# Utilities
from src.utils.models import TeamGralModel

STATUS = ((0, "Draft"), (1, "Publish"))

from src.utils.extra import upload_post_image_path


class Post(TeamGralModel):

    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True, editable=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at", "-updated_at"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)