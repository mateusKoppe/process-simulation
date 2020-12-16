import re

duration_regex = r"^TS=(\d+)$"


def is_duration(str):
    return re.search(duration_regex, str)


def generate_duration(raw):
    groups = re.search(duration_regex, raw).groups()

    return {
        "type": "duration",
        "value": int(groups[0]),
    }
