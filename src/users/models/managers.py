from datetime import timedelta
from django.utils import timezone

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import BaseUserManager


DEFAULT_ACTIVATION_DAYS = settings.DEFAULT_ACTIVATION_DAYS


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(email=self.normalize_email(email), **extra_fields)
        user_obj.set_password(password)  # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a created_at in here
        end_range = now
        return self.filter(activated=False, forced_expired=False).filter(
            created_at__gt=start_range, created_at__lte=end_range
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return (
            self.get_queryset()
            .filter(Q(email=email) | Q(user__email=email))
            .filter(activated=False)
        )
