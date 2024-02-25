import re


class Patterns:
    datetime = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"
    # plate = r"[A-Za-z]\d{3}-[A-Za-z]{2}\d{2,3}"
    plate = r"plate recognized: \w+ "
    enter = r"\'Вх\w+\'"
    exit = r"\'Вых\w+\'"
    line = datetime + r" [+-]\d{2}:\d{2} \[INF\]" + r".{1,}?" + enter
    jopa = r"(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) [+-]\d{2}:\d{2} \[INF\] (?P<enter>Вх[А-Яа-я]+: (plate (?P<plate>[\d\w]+ saved)))?"

