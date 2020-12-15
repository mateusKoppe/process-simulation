import re
from ..utils import format_next

entrance_regex = r"^G(\d):(\d+)-(\d+);([CRS]\d+)$"


def is_entrance(str):
    return re.search(entrance_regex, str)


def entrance_generate(raw):
    groups = re.search(entrance_regex, raw).groups()
    return {
        "type": "entrance",
        "id": int(groups[0]),
        "min": int(groups[1]),
        "max": int(groups[2]),
        "next": format_next(groups[3]),
    }
