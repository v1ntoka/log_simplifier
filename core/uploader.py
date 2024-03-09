from upload.models import UploadModel
from upload.forms import UploadForm


class Uploader(object):
    MAX_FILE_SIZE = 51 * 1024 * 1024
    MAX_FILES_COUNT = 10

    def __init__(self, request, *args, **kwargs):
        self.queryset = UploadModel.objects.all()
        self.request = request
        self.form = UploadForm(request.POST, request.FILES) if request.method == 'POST' else UploadForm()

    def _filename(self):
        name = self.request.FILES["File"].name
        obj = self.request.POST["obj"]
        return f"{name}__{obj}"

    def _have_duplicate(self, filename):
        return any(i.name == filename for i in self.queryset)

    def _get_oldest(self):
        return self.queryset.order_by("-date").first()

    def save(self):
        if self.form.is_valid():
            if self._have_duplicate(self._filename()):
                print('duplicate')
                UploadModel.objects.get(name=self._filename()).delete()
            elif len(self.queryset) == self.MAX_FILES_COUNT:
                print("a lot of")
                self._get_oldest().delete()
            self.form.save()
        else:
            raise Exception("Invalid upload")

    def __getattr__(self, item):
        return None
