"""Posts model."""
# Django
from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

# Utilities
from src.utils.models import GralModel

STATUS = ((0, "Draft"), (1, "Publish"))

from src.utils.extra import upload_post_image_path


class Post(GralModel):

    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.BinaryField(blank=True, null=True, editable=True)
    content_type = models.CharField(
        max_length=256, null=True, blank=True, help_text="The MIMEType of the file"
    )
    status = models.IntegerField(choices=STATUS, default=0)
    comments = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Comment", related_name="comments_owned"
    )
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Fav", related_name="favorite_ads"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})


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


class Comment(GralModel):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15:
            return self.text
        return self.text[:11] + " ..."


class Fav(GralModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return "%s likes %s" % (self.user.username, self.ad.title[:10])
