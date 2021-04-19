from django.views import generic
from django.urls import reverse_lazy
from django.http import request, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from src.users.forms import SignupForm, LoginForm, ReactivateEmailForm

from src.utils.mixins import NextUrlMixin, RequestFormAttachMixin
from src.users.models import EmailActivation


class AccountEmailActivateView(generic.edit.FormMixin, generic.View):
    success_url = reverse_lazy("users:login")
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(
                    request, "Your email has been confirmed. Please login."
                )
                return redirect("users:login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse_lazy("users:password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(
                        link=reset_link
                    )
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {"form": self.get_form(), "key": key}
        return render(request, "registration/activation-error.html", context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {"form": form, "key": self.key}
        return render(self.request, "registration/activation-error.html", context)


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

    def form_valid(self, form):
        msg = """Check Your Email To Activate Your Account!"""
        request = self.request
        messages.success(request, msg)        
        return super(SingupView, self).form_valid(form)