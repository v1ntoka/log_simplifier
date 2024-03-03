import re


class Patterns:
    datetime = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"
    # plate = r"[A-Za-z]\d{3}-[A-Za-z]{2}\d{2,3}"
    plate = r"plate recognized: (?P<plate>\S+) "
    enter = r"\'[\S]*(?P<enter>Вх\d*)[\S]*\'"
    exit = r"\'[\S]*(?P<exit>Вых\d*)[\S]*\'"
    entrance = r"[\S]*(?P<entrance>В[ы]?х\d*)[\S]*"
    line = datetime + r" [+-]\d{2}:\d{2} \[INF\]" + r".{1,}?" + enter
    datetime_entrance = r"(?P<datetime>^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).* [\S]*(?P<entrance>В[ы]?х\d*)[\S]*"
    datetime_plate = r"(?P<datetime>^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).* plate recognized: (?P<plate>\S+) "
    jopa = r"^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).+([\'\.][\S]*(?P<enterance>В[ы]?х\d?)[\S]*\'?)(\splate( (?P<plate>\S+)?(stored:(?P=plate)?|(saved to DB))?)?"

