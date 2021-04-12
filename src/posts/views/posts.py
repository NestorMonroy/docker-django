from django.views import View
from django.http import request
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.humanize.templatetags.humanize import naturaltime

# Models
from src.posts.models import Post

from src.posts.forms import PostCreateForm


class PostDetailView(generic.DetailView):
    queryset = Post.objects.all()
    template_name = "posts/post_detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")

        try:
            instance = Post.objects.get(slug=slug, status=0)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except:
            raise Http404("??")
        return instance


class PostCreateView(LoginRequiredMixin, View):
    template_name = "posts/ad_post.html"
    success_url = reverse_lazy("posts:all")

    def get(self, request, pk=None):
        form = PostCreateForm()
        ctx = {"form": form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = PostCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        post = form.save(commit=False)
        # import pdb ;pdb.set_trace()
        post.author = self.request.user.profile
        post.save()
        return redirect(self.success_url)


class PostListView(View):
    model = Post
    template_name = "posts/post_list.html"

    def get(self, request):
        objects = Post.objects.all().order_by("-updated_at")[:10]

        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {
            "post_list": objects,
        }

        return render(request, self.template_name, ctx)
