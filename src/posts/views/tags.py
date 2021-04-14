from django.views import generic
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from src.posts.models import Tag
from src.posts.forms import TagForm


@method_decorator(staff_member_required, name="dispatch")
class TagListView(generic.ListView):
    template_name = "tags/tag_list.html"
    model = Tag
    paginate_by = 20


    def get_queryset(self):
        qs = Tag.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Tags"
        context['tags'] = Tag.objects.all()
        context['tag_form'] = TagForm()
        return context


def tag_creation_view(request):
    form = TagForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f"Τhe tag {obj} was created!!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
