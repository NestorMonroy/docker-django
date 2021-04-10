from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect

from src.users.forms import SignupForm, LoginForm

from src.utils.mixins import NextUrlMixin, RequestFormAttachMixin


class LoginView(NextUrlMixin, RequestFormAttachMixin, generic.FormView):
    form_class = LoginForm
    success_url = "/"
    template_name = "users/login.html"
    default_next = "/"

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class SingupView(generic.CreateView):
    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("users:login")