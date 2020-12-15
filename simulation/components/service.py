import re
import random
from ..utils import format_next
from ..units import unit_update_next, add_unit

service_regex = r"^C(\d);(\d+);((\d+:\d+-\d+,?)+);([CRS]\d+)$"


def is_service(str):
    return re.search(service_regex, str)


def generate_service(raw):
    groups = re.search(service_regex, raw).groups()

    services_raw = groups[2].split(',')

    attendants = []
    for service_raw in services_raw:
        service_groups = re.search(
            r"^(\d+):(\d+)-(\d+)$", service_raw).groups()
        attendants.append({
            "id": int(service_groups[0]),
            "min": int(service_groups[1]),
            "max": int(service_groups[2]),
        })

    return {
        "type": "service",
        "id": int(groups[0]),
        "attendants": attendants,
        "next": format_next(groups[4]),
    }


def process_service(simulation, unit):
    _simulation = simulation.copy()

    component = _simulation["services"][unit["next"]["id"]]

    attendants = component["attendants"].copy()
    random.shuffle(attendants)

    interval = random.randint(
        attendants[0]["min"], attendants[0]["max"])

    when = interval + _simulation["clock"]
    if when > _simulation["clock_limit"]:
        _simulation["clock_limit"] = when

    _unit = unit_update_next(unit, component["next"], _simulation["clock"])
    _simulation["events"] = add_unit(_simulation["events"], _unit, when)
    return _simulation
