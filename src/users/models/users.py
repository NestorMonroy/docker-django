""" User model"""
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import pre_save, post_save

from django.core.mail import send_mail
from django.template.loader import get_template

from src.utils.models import GralModel
from src.utils.extra import unique_key_generator
from .managers import UserManager, EmailActivationManager


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

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_verified = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = settings.BASE_URL
                key_path = reverse(
                    "users:email-activate", kwargs={"key": self.key}
                )  # use reverse
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {"path": path, "email": self.email}
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = "1-Click Email Verification"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                e_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
                )
                return e_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()


post_save.connect(post_save_user_create_reciever, sender=User)
