from upload.models import UploadModel
from upload.forms import UploadForm


class InvalidFileError(Exception):
    ...


class Uploader(object):
    # MAX_FILE_SIZE = 51 * 1024 * 1024 пока решил не валидировать размер, плюс его можно настраивать напрямую на nginx
    MAX_FILES_COUNT = 10

    def __init__(self, request, *args, **kwargs):
        self.queryset = UploadModel.objects.all()
        self.request = request
        self.form = UploadForm(request.POST, request.FILES) if request.method == 'POST' else UploadForm()

    def _filename(self):
        name = self.request.FILES["File"].name.split('.')[0]
        obj = self.request.POST["obj"]
        return f"{name}__{obj}"

    def _have_duplicate(self, filename):
        return any(i.name == filename for i in self.queryset)

    def _get_oldest(self):
        return self.queryset.order_by("-date").first()

    def save(self):
        if self.form.is_valid():
            if self._have_duplicate(self._filename()):
                UploadModel.objects.get(name=self._filename()).delete()
            elif len(self.queryset) == self.MAX_FILES_COUNT:
                self._get_oldest().delete()
            self.form.save()
        else:
            raise InvalidFileError(self.form.errors)

    def __getattr__(self, item):
        return None
