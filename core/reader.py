import re
import datetime as dt

from core.regex import Patterns
from upload.models import UploadModel
from django.utils import timezone
from dataclasses import dataclass

MAX_COUNTER_UNFOUNDED = 10


@dataclass
class Flags:
    loop_a: bool = False
    loop_b: bool = False
    barrier_down: bool = False
    counter_loop_b: int = 0
    counter_barrier_down: int = 0

    def values(self) -> tuple[bool, bool, bool]:
        return self.loop_a, self.loop_b, self.barrier_down

    def flags(self) -> tuple[int, int]:
        return self.counter_loop_b, self.counter_barrier_down

def _get_file(filename: str) -> UploadModel.File:
    """Возвращает файл из базы данных по имени, попутно обновляя дату-время последнего открытия"""
    file = UploadModel.objects.get(name=filename)
    file.date = timezone.now()
    file.save(date_update=True)
    return file


class Reader:
    def __init__(self, filename: str, *args, **kwargs):
        self.file: UploadModel.File = _get_file(filename)

        with open(self.file.File.path, 'r', encoding='utf-8') as logfile:
            self.text: list[str] = [i for i in logfile.readlines()]

        self.args = args
        self.filters: dict = {}
        self._kwargs_processing(kwargs)

    def _kwargs_processing(self, kwargs) -> None:
        """Приводит кварги к более удобной для взаимодействия форме"""
        for key in kwargs:
            if key != 'csrfmiddlewaretoken':
                if key in ('date_before', 'date_after') and kwargs[key] != ['']:
                    kwarg = dt.datetime.fromisoformat(kwargs[key][0])
                    setattr(self, key, kwarg)
                    self.filters[key] = kwargs[key][0]
                else:
                    kwarg = kwargs[key][0].strip()
                    setattr(self, key, kwarg)
                    self.filters[key] = kwarg

    def _extra_filter(self) -> None:
        """Выполняется приоритетнее всего.
        Включает в выдачу только строки, в которых сработало введенное регулярное выражение"""
        res: list[str] = []
        for line in self.text:
            if re.search(getattr(self, 'extra', ''), line):
                res.append(line)
        self.text = res

    def _plate_filter(self) -> None:
        """Если фильтры были проставлены вручную(например дата и время), то сначала отработают они,
        только потом выставятся новые"""
        match: int = 0
        res: list[str] = []
        flags: Flags = Flags()

        # if getattr(self, 'date_before', None) or getattr(self, 'date_after', None):
        #     self._date_filter()
        # if getattr(self, 'entrance', None):
        #     self._entrance_filter()

        for line in self.text:
            if re.search(getattr(self, 'plate', ''), line):
                # Запоминаем, где найдена машина
                search = re.search(Patterns.entrance, line)
                if search is not None:
                    setattr(self, 'entrance', search.group('entrance'))
                    break

        if getattr(self, 'entrance', None):
            # Во всех логах ищем те, которые связаны исключительно с въездом-выездом, где найдена машина
            self._entrance_filter()
            for index, line in enumerate(self.text):
                if re.search(getattr(self, 'plate', ''), line):
                    # Запоминаем, по какому индексу обнаружен номер
                    match = index
                    break

            for line in self.text[match:0:-1]:
                res.append(line)
                if re.search(Patterns.loop_a, line):
                    # Добавляем все логи выше найденного индекса пока не сработает петля А
                    flags.loop_a = True
                    break

            res = res[::-1]

            for line in self.text[match + 1 if match + 1 != len(res) else match:]:
                res.append(line)
                if re.search(Patterns.loop_b, line):
                    # аналогично предыдущему шагу, но с петлей Б
                    flags.loop_b = True

                if re.search(Patterns.barrier_down, line):
                    # удостоверяемся что шб закрыт(хотя бы по логам лол)
                    flags.barrier_down = True

                if flags.loop_b and not flags.barrier_down:
                    flags.counter_loop_b += 1

                if flags.barrier_down and not flags.loop_b:
                    print(flags.flags())
                    flags.counter_barrier_down += 1

                if all(flags.values()):
                    break

                if flags.counter_loop_b == MAX_COUNTER_UNFOUNDED:
                    res.append(
                        f'<span style="color:red">НЕ НАЙДЕНО ИНФОРМАЦИИ О ЗАКРЫТИИ ШЛАГБАУМА БОЛЕЕ ЧЕМ В {MAX_COUNTER_UNFOUNDED} СТРОКАХ ПОСЛЕ ПЕТЛИ Б</span>')
                    break

                if flags.counter_barrier_down == MAX_COUNTER_UNFOUNDED:
                    res.append(
                        f'<span style="color:red">НЕ НАЙДЕНО ИНФОРМАЦИИ О ПЕТЛЕ Б БОЛЕЕ ЧЕМ В {MAX_COUNTER_UNFOUNDED} СТРОКАХ ПОСЛЕ ЗАКРЫТИЯ ШЛАГБАУМА</span>')
                    break

        self.text = res

    def _date_filter(self) -> None:
        res: list[str] = []
        if getattr(self, 'date_before', None) and getattr(self, 'date_after', None):
            for line in self.text:
                if (search := re.search(Patterns.datetime, line)) and \
                        (getattr(self, 'date_before') <= dt.datetime.fromisoformat(search.group('datetime'))
                         <= getattr(self, 'date_after')):
                    res.append(line)
        elif getattr(self, 'date_before', None):
            for line in self.text:
                if (search := re.search(Patterns.datetime, line)) and \
                        getattr(self, 'date_before') \
                        <= dt.datetime.fromisoformat(search.group('datetime')):
                    res.append(line)
        elif getattr(self, 'date_after', None):
            for line in self.text:
                if (search := re.search(Patterns.datetime, line)) and \
                        getattr(self, 'date_after') \
                        <= dt.datetime.fromisoformat(search.group('datetime')):
                    res.append(line)
        self.text = res

    def _entrance_filter(self) -> None:
        res: list[str] = []
        for line in self.text:
            if (search := re.search(Patterns.entrance, line)) and (
                    search.group('entrance') == getattr(self, 'entrance')):
                res.append(line)
        self.text = res

    def read(self) -> list[str]:
        if getattr(self, 'extra', None):
            self._extra_filter()
        if any((getattr(self, 'date_before', None), getattr(self, 'date_after', None))):
            self._date_filter()
        if getattr(self, 'entrance', None):
            self._entrance_filter()
        if getattr(self, 'plate', None):
            self._plate_filter()

        return self.text
