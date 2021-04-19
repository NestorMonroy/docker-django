""" User model"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from src.utils.models import GralModel
from .managers import UserManager


class User(PermissionsMixin, GralModel, AbstractBaseUser):
    """User model.
    Extend from Django's Abstract User, change the username field to email and
    add some extra fields
    """

    email = models.EmailField(
        "email addres",
        unique=True,
        error_messages={"unique": "A user with email already exists"},
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    is_client = models.BooleanField(
        "client ",
        default=True,
        help_text=(
            "Help easily distinguish user and perfom queris."
            "Clients are the main type of user"
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        "verified",
        default=False,
        help_text="Set to True when the user have verified its email addres ",
    )

    objects = UserManager()

    def __str__(self):
        """Return email. """
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return email. """
        return self.email


class EmailActivation(GralModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)  # 7 Days

    def __str__(self):
        return self.email