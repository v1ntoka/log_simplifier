from django import forms as f
from upload.models import UploadModel



# class UploadForm(f.Form):
#
#     file = f.FileField(
#         label='Upload File',
#         widget=f.ClearableFileInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         ),
#         validators=[file_size]
#     )

class UploadForm(f.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UploadModel
        fields = ['File', "obj"]

    # def clean(self):
    #     cleaned_data = super(UploadForm, self).clean()
    #     if 'File' in cleaned_data:
    #         return cleaned_data