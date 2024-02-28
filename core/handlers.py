import re
from core.regex import Patterns
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile, UploadedFile
import os
import datetime as dt
from dataclasses import dataclass

MEDIA_URL = "media/"
NAME_DATE_DIVIDER = "__"
DATE_PART_DIVIDER = "_"
TIME_PART_DIVIDER = "+"
FILE_SAVE_MASK = f"%Y{DATE_PART_DIVIDER}%m{DATE_PART_DIVIDER}%dT%H{TIME_PART_DIVIDER}%M{TIME_PART_DIVIDER}%S"
MAX_FILES_COUNT = 10


@dataclass
class FilesListElement:
    original_name: str
    date: dt.datetime
    file_name: str
    href: str


def filename_handler(name, return_name_wo_date=False) -> tuple[str, dt.datetime]:
    name_ret = name.split(NAME_DATE_DIVIDER)[0] if return_name_wo_date else name
    date = name.split(NAME_DATE_DIVIDER)[1].replace(DATE_PART_DIVIDER, '-').replace(TIME_PART_DIVIDER, ':')
    return name_ret, dt.datetime.fromisoformat(date)


def delete_oldest_file():
    date_files = {}
    for i in os.listdir(MEDIA_URL):
        if os.path.isfile(MEDIA_URL + i):
            name, date = filename_handler(i)
            date_files[date] = name
    os.remove(f"{MEDIA_URL}{date_files[min(date_files)]}")


def get_files_list() -> list[FilesListElement]:
    ret = []
    for file in os.listdir(MEDIA_URL):
        if os.path.isfile(MEDIA_URL + file):
            name, date = filename_handler(file, return_name_wo_date=True)
            href = name.split('.')[0]
            ret.append(FilesListElement(name, date, file, href))
    ret.sort(key=lambda x: x.date)
    return ret


def actualize_filename(name: FilesListElement):
    now = dt.datetime.now().strftime(FILE_SAVE_MASK)
    new_name = name.original_name + NAME_DATE_DIVIDER + now
    os.rename(MEDIA_URL + name.file_name, MEDIA_URL + new_name)


def save_file_handler(file: UploadedFile):
    if file.name not in (i.original_name for i in get_files_list()):
        if len(os.listdir(MEDIA_URL)) >= 10:
            delete_oldest_file()
        now = dt.datetime.now().strftime(FILE_SAVE_MASK)
        text = file.chunks()
        with open(f"{MEDIA_URL}{file.name}{NAME_DATE_DIVIDER}{now}", 'wb') as saved_file:
            for line in text:
                saved_file.write(line)
    else:
        for i in get_files_list():
            if i.original_name == file.name:
                actualize_filename(i)


def kwargs_preparing(kwargs) -> dict:
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


def text_filter(file_text: list, **kwargs) -> list[str]:
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
