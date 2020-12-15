import re
import random
from ..utils import format_next
from ..units import unit_update_next, add_unit

service_regex = r"^C(\d);(\d+);((\d+:\d+-\d+,?)+);([CRS]\d+)$"


def is_service(str):
    return re.search(service_regex, str)


def service_generate(raw):
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


def process_service(simulation, units, unit, clock):
    component = simulation["services"][unit["next"]["id"]]
    interval = random.randint(
        component["attendants"][0]["min"], component["attendants"][0]["max"])
    when = interval + clock
    _unit = unit_update_next(unit, component["next"], clock)
    _units = add_unit(units, _unit, when)
    return _units, when
