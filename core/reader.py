import os
import re

from core import handlers
from core.regex import Patterns
import datetime as dt


# noinspection PyAttributeOutsideInit
class Reader:
    _media_url = 'media/'

    def __init__(self, filename: str, *args, **kwargs):
        self.text: str | list[str]
        self.filename = filename
        self.args = args
        self._kwargs_processing(kwargs)

    def _kwargs_processing(self, kwargs) -> None:

        for file in handlers.get_files_list():
            if file.href == self.filename:
                self.file = file
                self.file.file_name = handlers.actualize_filename(self.file)

        for key in kwargs:
            if key != 'csrfmiddlewaretoken':
                if key in ('date_before', 'date_after') and kwargs[key] != ['']:
                    setattr(self, key, dt.datetime.fromisoformat(kwargs[key][0]))
                else:
                    setattr(self, key, kwargs[key][0])

        if self.date_before and not self.date_after:
            self.date_after = self.date_before + dt.timedelta(milliseconds=60000)
        elif self.date_after and not self.date_before:
            self.date_before = self.date_after - dt.timedelta(milliseconds=60000)

    def datetime_filter(self, logfile, current_datetime: None | dt.datetime = None) -> str | list[str]:
        """Параметр current_datetime используется если уже изначально задан
        промежуток времени в фильтрах. Функция заменит данные в фильтрах"""
        if current_datetime:
            self.date_before = current_datetime - dt.timedelta(milliseconds=10000)
            self.date_after = current_datetime + dt.timedelta(milliseconds=10000)

    def plate_filter(self, logfile) -> str | list[str]:
        result = []
        for line in logfile:
            if (match := re.search(Patterns.datetime_plate, line)) and match.group('plate') == self.plate:
                self.entrance = re.search(Patterns.entrance, line).group('entrance')
                self.datetime_filter(logfile, dt.datetime.fromisoformat(match.group('datetime')))
                print(self.date_after, self.date_before)
                break
        logfile.seek(0)
        for line in logfile:
            # if (match := re.search(Patterns.entrance, line)) and match.group('entrance') == self.entrance:
            if (match := re.search(Patterns.datetime_entrance, line)) and match.group('entrance') == self.entrance:
                if self.date_before and self.date_before <= dt.datetime.fromisoformat(match.group('datetime')) <= self.date_after:
                    result.append(line)
        return result if result else ''

    def text_filter(self, logfile) -> str | list[str]:
        if self.plate and not self.date_before:
            return self.plate_filter(logfile)
        else:
            return logfile.readlines()

    def read(self) -> str | list[str]:
        if os.path.exists(self._media_url + self.file.file_name):
            with open(self._media_url + self.file.file_name, 'r', encoding='utf-8') as logfile:
                self.text = self.text_filter(logfile)
            return self.text
        else:
            raise FileNotFoundError('File does not exists')

    def __getattr__(self, item):
        return None
