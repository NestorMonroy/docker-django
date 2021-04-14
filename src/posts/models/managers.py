from django.db import models
from django.db.models import Q


class PostQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status=1)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups).distinct()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)
