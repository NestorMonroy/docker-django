from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile

from src.posts.models import Post
from .humanize import naturalsize


class PostCreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'image' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    image = forms.FileField(
        required=False, label="File to Upload <= " + max_upload_limit_text
    )
    upload_field_name = "image"

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Post
        fields = ["title", "content", "image", "status"]  # image is manual

    # Validate the size of the image
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

        # We only need to adjust image if it is a freshly uploaded file
        f = instance.image  # Make a copy
        if isinstance(
            f, InMemoryUploadedFile
        ):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.image = bytearr  # Overwrite with the actual image data
        # import pdb ;pdb.set_trace()
        if commit:
            instance.save()

        return instance