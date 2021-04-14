from django.views import generic
from django.http import request, HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.humanize.templatetags.humanize import naturaltime

from src.posts.models import Post, Comment
from src.posts.forms import PostCreateForm, CommentForm
from src.utils import owner, mixins as post_mixins
from src.utils.mixins import ContextPostSlugMixin


class PostDeleteView(post_mixins.ContextPostSlugMixin, owner.AuthorDeleteView):
    model = Post
    success_url = reverse_lazy("posts:all")


def stream_file(request, slug):
    pic = get_object_or_404(Post, slug=slug)
    response = HttpResponse()
    response["Content-Type"] = pic.content_type
    response["Content-Length"] = len(pic.image)
    response.write(pic.image)
    return response


class PostDetailView(post_mixins.ContextPostSlugMixin, generic.DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get(self, request, slug):
        x = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=x).order_by("-updated_at")
        comment_form = CommentForm()
        context = {"post": x, "comments": comments, "comment_form": comment_form}
        return render(request, self.template_name, context)


class PostUpdateView(LoginRequiredMixin, generic.View):
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("posts:all")

    def get(self, request, slug):

        slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug, author=self.request.user)
        form = PostCreateForm(instance=post)
        ctx = {"form": form}
        # import pdb ;pdb.set_trace()
        return render(request, self.template_name, ctx)

    def post(self, request, slug=None):
        slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug, author=self.request.user)
        form = PostCreateForm(request.POST, request.FILES or None, instance=post)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        post = form.save(commit=False)
        post.save()

        return redirect(self.success_url)


class PostCreateView(LoginRequiredMixin, generic.View):
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("posts:all")

    def get(self, request, slug=None):
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
        post.author = self.request.user
        post.save()
        return redirect(self.success_url)


class PostListView(generic.View):
    model = Post
    template_name = "posts/post_list.html"

    def get(self, request):
        objects = Post.objects.filter(status=1).order_by("-updated_at")[:10]

        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {
            "post_list": objects,
        }

        return render(request, self.template_name, ctx)



class CommentCreateView(LoginRequiredMixin, generic.View):
    def post(self, request, slug):
        a = get_object_or_404(Post, slug=slug)
        comment = Comment(
            text=request.POST['comment'], owner=request.user, post=a)
        comment.save()
        return redirect(reverse('posts:post_detail', args=[slug]))