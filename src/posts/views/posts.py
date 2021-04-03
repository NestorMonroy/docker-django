from django.views import View
from django.http import request
from django.views import generic
from django.shortcuts import render

from django.contrib.humanize.templatetags.humanize import naturaltime

#Models
from src.posts.models import Post


class AdListView(View):
    model = Post
    template_name = "posts/post_list.html"

    def get(self, request):
        objects = Post.objects.all().order_by('-modified')[:10]

        for obj in objects:
            obj.natural_updated = naturaltime(obj.modified)

        ctx = {
            'post_list': objects,
        }

        return render(request, self.template_name, ctx)
