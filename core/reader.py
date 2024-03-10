import re
import datetime as dt

from core.regex import Patterns
from upload.models import UploadModel
from django.utils import timezone


def _get_file(filename: str):
    file = UploadModel.objects.get(name=filename)
    file.date = timezone.now()
    file.save(date_update=True)
    return file


class Reader:
    def __init__(self, filename: str, *args, **kwargs):
        self.file = _get_file(filename)
        self.text = [i.decode('utf-8') for i in self.file.File.readlines()]
        self.args = args
        self._kwargs_processing(kwargs)

    def _kwargs_processing(self, kwargs) -> None:
        for key in kwargs:
            if key != 'csrfmiddlewaretoken':
                if key in ('date_before', 'date_after') and kwargs[key] != ['']:
                    setattr(self, key, dt.datetime.fromisoformat(kwargs[key][0]))
                else:
                    setattr(self, key, kwargs[key][0].strip())

    def _extra_filter(self):
        res = []
        for line in self.text:
            if re.search(getattr(self, 'extra', ''), line):
                res.append(line)
        self.text = res

    def _plate_filter(self):
        ...

    def _date_filter(self):
        ...

    def _entrance_filter(self):
        ...

    def read(self, *args, **kwargs) -> list[str]:
        if getattr(self, 'extra', None):
            self._extra_filter()
        if getattr(self, 'plate', None):
            self._plate_filter()
        if any((getattr(self, 'date_before', None), getattr(self, 'date_after', None))):
            self._date_filter()
        if getattr(self, 'entrance', None):
            self._entrance_filter()
        return self.text
