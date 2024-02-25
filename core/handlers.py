import re
from core.regex import Patterns
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
import os
import datetime as dt


def create_temp_file(file):
    logfile = None
    if isinstance(file, TemporaryUploadedFile):
        logfile = open(file.temporary_file_path(), 'r', encoding='utf-8')
    elif isinstance(file, InMemoryUploadedFile):
        logfile = bytes.decode(file.read()).split('\n')

    with open('temp_file.txt', 'w', encoding='utf-8') as temp:
        for line in logfile:
            temp.write(line)
    if isinstance(file, TemporaryUploadedFile):
        file.close()


def kwargs_preparing(kwargs):
    res = {}
    for key in kwargs:
        if key != 'csrfmiddlewaretoken':
            if key in ('date_before', 'date_after') and kwargs[key][0] != '':
                res[key] = dt.datetime.fromisoformat(kwargs[key][0])
            else:
                res[key] = kwargs[key][0]
    if res.get('date_before') and not res.get('date_after'):
        res['date_after'] = res.get('date_before') + dt.timedelta(milliseconds=999)
    elif res.get('date_after') and not res.get('date_before'):
        res['date_before'] = res.get('date_after') - dt.timedelta(milliseconds=999)
    return res


def text_filter(file_text: list, **kwargs):
    output = []
    for line in file_text:
        if kwargs.get('date_before'):
            if match := re.match(Patterns.datetime, line):
                date = dt.datetime.fromisoformat(match.group(0))
                if kwargs.get('date_before') < date < kwargs.get('date_after'):
                    output.append(line)
        else:
            output = file_text
    return output


def file_reader(**kwargs):
    if os.path.exists('temp_file.txt'):
        return text_filter(open('temp_file.txt', 'r', encoding='utf-8').readlines(), **kwargs_preparing(kwargs))
    else:
        print("File does not exist")
