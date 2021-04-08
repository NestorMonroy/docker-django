from django import forms
from django.contrib.auth import get_user_model
from django.contrib import messages

# Models
from src.users.models import Profile

User = get_user_model()


class SignupForm(forms.ModelForm):

    """Sign up form."""

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "placeholder": "email",
                "class": "form-control",
                "required": True,
            }
        ),
    )

    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "placeholder": "Username",
                "class": "form-control",
                "required": True,
            }
        ),
    )

    first_name = forms.CharField(
        min_length=3,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "id": "first_name",
                "placeholder": "First name",
                "class": "form-control",
                "required": True,
            }
        ),
    )

    last_name = forms.CharField(
        min_length=3,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "id": "last_name",
                "placeholder": "Last name",
                "class": "form-control",
                "required": True,
            }
        ),
    )

    password = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "placeholder": "Password",
                "class": "form-control",
                "required": True,
            }
        ),
    )

    confirmation = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "id": "confirmation",
                "placeholder": "Password Confirmation",
                "class": "form-control",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
        )

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
        print(user)
        user.is_active = False
        if commit:
            user.save()
        return user