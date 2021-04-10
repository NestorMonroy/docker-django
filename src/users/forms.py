from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.validators import RegexValidator
from django.contrib import messages

# Models
from src.users.models import Profile

from .signals import user_logged_in

User = get_user_model()


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
                pass
                ## not active, check email activation

        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        user_logged_in.send(user.__class__, instance=user, request=request)
        self.user = user
        #import pdb ;pdb.set_trace()
        return data


class SignupForm(forms.ModelForm):

    """Sign up form."""

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={"required": True}),
    )

    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"required": True}),
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

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +1234567890 Up to 15 digits allowed.",
    )

    phone_number = forms.CharField(validators=[phone_regex])

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
        fields = ("email", "username", "first_name", "last_name", "phone_number")

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