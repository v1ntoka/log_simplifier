class Patterns:
    datetime = r"^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})"
    plate = r"plate recognized: (?P<plate>\S+) "
    entrance = r"[\S]*(?P<entrance>В[ы]?х\d*)[\S]*"
    datetime_entrance = r"(?P<datetime>^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).* [\S]*(?P<entrance>В[ы]?х\d*)[\S]*"
    datetime_plate = r"(?P<datetime>^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).* plate recognized: (?P<plate>\S+) "
    loop_a = r"ПетляА|ПетА"
    loop_b = r"ПетляБ|ПетБ"
