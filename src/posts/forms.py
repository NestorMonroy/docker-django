from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from src.posts.models import Post, Tag
from .humanize import naturalsize


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            "title",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)


class PostCreateForm(forms.ModelForm):
    STATUS = ((0, "Draft"), (1, "Publish"))

    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'image' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    image = forms.FileField(
        required=False, label="File to Upload <= " + max_upload_limit_text
    )
    upload_field_name = "image"
    status = forms.ChoiceField(required=True, choices=STATUS)
    #tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Post
        tags = forms.ModelChoiceField(queryset=Tag.objects.all())
        fields = ["title", "content", "image", "status", "tags"]  # image is manual
        # widgets = {
        #     "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        # }

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get("image")
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error(
                "image", "File must be < " + self.max_upload_limit_text + " bytes"
            )

    # Convert uploaded File object to a image
    def save(self, commit=True):
        instance = super(PostCreateForm, self).save(commit=False)
        # tags = self.cleaned_data["tags"]
        # We only need to adjust image if it is a freshly uploaded file
        f = instance.image  # Make a copy
        if isinstance(
            f, InMemoryUploadedFile
        ):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.image = bytearr  # Overwrite with the actual image data
        # instance.tags = self.cleaned_data["tags"]
        # self.save_m2m()
        # import pdb ;pdb.set_trace()
        if commit:
            instance.save()

        import pdb

        # pdb.set_trace()
        return instance