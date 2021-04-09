from django.views import generic
from django.urls import reverse_lazy

from src.users.forms import SignupForm


class SingupView(generic.CreateView):
    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("posts:all")