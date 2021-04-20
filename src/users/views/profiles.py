from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from src.users.models import Profile, User

from src.users.forms import ProfileDetailChangeForm, UserDetailChangeForm


@login_required
def profile_detail_update(request):
    path = "profile/detail-update-view.html"
    profile = request.user.profile
    user = request.user
    # profile = get_object_or_404(Profile, user=request.user)
    # user = get_object_or_404(User, id=request.user.id)
    # user = get_object_or_404(User, id=request.user.id)

    if request.method == "POST":
        profile_form = ProfileDetailChangeForm(
            request.POST, request.FILES or None, instance=profile
        )
        user_form = UserDetailChangeForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_data = profile_form.cleaned_data
            user_data = user_form.cleaned_data

            profile.biography = profile_data["biography"]
            user.first_name = user_data["first_name"]
            user.last_name = user_data["last_name"]
            profile.save()
            user.save()
            return HttpResponseRedirect(reverse("profile:user-update"))
        else:
            ctx = {"profile_form": profile_form, "user_form": user_form}
            return render(request, self.template_name, ctx)

    else:
        profile_form = ProfileDetailChangeForm(instance=profile)
        user_form = UserDetailChangeForm(instance=user)
        ctx = {"profile_form": profile_form, "user_form": user_form}

    return render(request, path, ctx)


# class ProfileDetailUpdateView(LoginRequiredMixin, generic.View):
#     template_name = "profile/detail-update-view.html"
#     success_url = reverse_lazy("profile:user-update")

#     def get(self, request):
#         profile = get_object_or_404(Profile, user=self.request.user)
#         user = get_object_or_404(User, id=self.request.user.id)
#         form_profile = ProfileDetailChangeForm(instance=profile)
#         form_user = UserDetailChangeForm(instance=user)
#         ctx = {"form_profile": form_profile, "form_user": form_user}
#         return render(request, self.template_name, ctx)

#     def post(self, request):
#         form_profile = ProfileDetailChangeForm(request.POST)
#         form_user = UserDetailChangeForm(request.POST)

#         if not form.is_valid():
#             ctx = {"form_profile": form_profile, "form_user": form_user}
#             return render(request, self.template_name, ctx)

#         return redirect(self.success_url)


class ProfileHomeView(LoginRequiredMixin, generic.DetailView):
    template_name = "profile/home.html"

    def get_object(self):
        return self.request.user
