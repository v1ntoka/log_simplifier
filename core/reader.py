import os
import re

from core import handlers
from core.regex import Patterns


class Reader:
    _media_url = 'media/'

    def __init__(self, filename: str, *args, **kwargs):
        self.text: str | list[str]
        self.filename = filename
        self.args = args
        for file in handlers.get_files_list():
            if file.href == self.filename:
                self.file = file
                self.file.file_name = handlers.actualize_filename(self.file)
        for k, v in kwargs.items():
            if k != 'csrfmiddlewaretoken':
                setattr(self, k, v[0].strip())
                # self.__dict__[k] = v
        print(self.__dict__)

    def plate_filter(self, logfile) -> str | list[str]:
        result = []
        entrance, enter, ext = None, None, None
        for line in logfile:
            if self.plate in line:
                if match := re.match(Patterns.plate, line) and match.group('plate') == getattr(self, 'plate'):
                    if match := re.match(Patterns.enter, line):
                        setattr(self, 'enter', match.group('enter'))
                        print(match.group('enter'))
                    if match := re.match(Patterns.exit, line):
                        setattr(self, 'exit', match.group('exit'))
                        print(match.group('exit'))

        logfile.seek(0)
        if enter := getattr(self, 'enter', None) and (ext := getattr(self, 'exit', None)):
            entrance = getattr(self, 'enter'), getattr(self, 'exit')
        else:
            if enter:
                entrance = enter,
            elif ext:
                entrance = ext,
        print(entrance)
        for line in logfile:
            if match := re.match(Patterns.enter, line):  # and match.group('entrance') in entrance:
                result.append(line)
                print('jopa')
        return result if result else ''

    def textfilter(self, logfile) -> str | list[str]:
        if getattr(self, 'plate', None):
            return self.plate_filter(logfile)
        else:
            return logfile.readlines()

    def read(self) -> str | list[str]:
        if os.path.exists(self._media_url + self.file.file_name):
            with open(self._media_url + self.file.file_name, 'r', encoding='utf-8') as logfile:
                self.text = self.textfilter(logfile)
            return self.text
        else:
            raise FileNotFoundError('File does not exists')
