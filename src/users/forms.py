from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.validators import RegexValidator
from django.contrib import messages
from django.utils.safestring import mark_safe

# Models
from src.users.models import Profile, EmailActivation

from .signals import user_logged_in

User = get_user_model()


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("users:signup")
            msg = """This email does not exists, would you like to <a href="{link}">register</a>?
            """.format(
                link=register_link
            )
            raise forms.ValidationError(mark_safe(msg))
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ## not active, check email activation
                link = reverse("users:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(
                    resend_link=link
                )
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = (
                        "Please check your email to confirm your account or "
                        + reconfirm_msg.lower()
                    )
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(
                    email
                ).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        self.user = user
        return data


class SignupForm(forms.ModelForm):

    """Sign up form."""

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={"required": True}),
    )

    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"required": True}),
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={"required": True}),
    )

    password = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.PasswordInput(attrs={"required": True}),
    )

    confirmation = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.PasswordInput(attrs={"required": True}),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_confirmation(self):
        """ Verify password confirmation match """
        data = super().clean()
        password = data["password"]
        confirmation = data["confirmation"]
        if password != confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return data

    def save(self, commit=True):

        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_verified = False
        if commit:
            user.save()

        profile = Profile(user=user)
        profile.save()
        return user