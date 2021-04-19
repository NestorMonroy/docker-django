from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin



class ProfileHomeView(LoginRequiredMixin, generic.DetailView):
    template_name = "profile/home.html"

    def get_object(self):
        return self.request.user
