from django.http import JsonResponse
from django.views import generic
from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from src.posts.models import Tag
from src.posts.forms import TagForm


class SearchTagView(generic.ListView):
    template_name = "tags/tag_list.html"

    def get(self, request, pk):
        tags = Tag.objects.all()
        post_tags = Tag.objects.filter(pk=pk)

        for tag in post_tags:
            tag = tag.tag_post.all()

        ctx = {"tag_result": tag, "tag_list": tags}

        return render(request, self.template_name, ctx)


@method_decorator(staff_member_required, name="dispatch")
class TagListView(generic.ListView):
    template_name = "tags/tag_list_create.html"
    # model = Tag
    paginate_by = 20

    def get_queryset(self):
        qs = Tag.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Tags"
        context["tags"] = Tag.objects.all()
        context["tag_form"] = TagForm()
        return context


def tag_creation_view(request):
    form = TagForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f"Τhe tag {obj} was created!!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@staff_member_required
def update_or_delete_tag_view(request, pk, action):
    obj = get_object_or_404(Tag, id=pk)
    if action == "delete":
        obj.delete()
    elif action == "update":
        form = TagForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {obj}")
        else:
            messages.warning(request, form.errors)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@staff_member_required
def ajax_update_tag_view(request, pk):

    obj = get_object_or_404(Tag, id=pk)
    form = TagForm(instance=obj)
    data = {}
    data["result"] = render_to_string(
        "tags/ajax_modal.html",
        request=request,
        context={
            "form": form,
            "form_title": f"finish {obj.title}",
            "form_action": reverse(
                "posts:tag_edit_or_update",
                kwargs={"pk": obj.id, "action": "update"},
            ),
            "delete_url": reverse(
                "posts:tag_edit_or_update",
                kwargs={"pk": obj.id, "action": "delete"},
            ),
        },
    )
    return JsonResponse(data)
