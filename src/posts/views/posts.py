from django.views import generic
from django.http import request, HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from django.contrib.humanize.templatetags.humanize import naturaltime

from src.posts.models import Post, Comment, Fav, Tag
from src.posts.forms import PostCreateForm, CommentForm, TagForm
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
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'

    def get(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        instance = Post.objects.get_by_slug(slug)
        favorites = list()
        comments = Comment.objects.filter(post=instance).order_by("-updated_at")
        comment_form = CommentForm()

        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_post.values("id")
            # favorites = [2, 4, ...] using list comprehension
            favorites = [row["id"] for row in rows]

        context = {
            "post": instance,
            "comments": comments,
            "comment_form": comment_form,
            "favorites": favorites,
        }

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

        tags = [s for s in form.cleaned_data["tags"]]
        post.tags.clear()
        if tags:
            # get/create tags and add them to the part
            for tag in tags:
                tag, created = Tag.objects.get_or_create(title=tag)
                post.tags.add(tag)

        print(tags)

        post.save()
        # import pdb ;pdb.set_trace()
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

        tags = [s for s in form.cleaned_data["tags"]]
        post.author = self.request.user

        if tags:
            post.save()

            for tag in tags:
                tag, create = Tag.objects.get_or_create(title=tag)
                post.tags.add(tag)
        # import pdb ;pdb.set_trace()
        post.save()
        return redirect(self.success_url)


class PostListView(generic.View):
    model = Post
    template_name = "posts/post_list.html"

    def get(self, request):
        objects = Post.objects.filter(status=1).order_by("-updated_at")
        tags = Tag.objects.all()
        query = request.GET.get("search", False)
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        if query:
            objects = Post.objects.search(query)

        else:
            objects = Post.objects.all().order_by("-updated_at")
        ctx = {"post_list": objects, "search": query, "tag_list": tags}
        # import pdb ;pdb.set_trace()
        return render(request, self.template_name, ctx)


class CommentCreateView(LoginRequiredMixin, generic.View):
    def post(self, request, slug):
        a = get_object_or_404(Post, slug=slug)
        comment = Comment(text=request.POST["comment"], owner=request.user, post=a)
        comment.save()
        return redirect(reverse("posts:post_detail", args=[slug]))


class CommentDeleteView(owner.OwnerDeleteView):
    model = Comment
    template_name = "posts/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        post = self.object.post
        return reverse("posts:post_detail", args=[post.slug])


@method_decorator(csrf_exempt, name="dispatch")
class AddFavoriteView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        # print("Post PK", pk)
        post = get_object_or_404(Post, id=pk)
        fav = Fav(user=request.user, post=post)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class DeleteFavoriteView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        # print("Delete PK", pk)
        post = get_object_or_404(Post, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, post=post).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
