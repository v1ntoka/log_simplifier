from django import forms as f


class UploadForm(f.Form):
    file = f.FileField(
        label='Upload File'
    )
