from django import forms as f
from core.fields import ContentTypeRestrictedFileField
from core.validators import file_size


class UploadForm(f.Form):
    # file = ContentTypeRestrictedFileField(
    #     label='Upload File',
    #     max_upload_size=51 * 1024 * 1024
    # )
    file = f.FileField(
        label='Upload File',
        widget=f.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        validators=[file_size]
    )
