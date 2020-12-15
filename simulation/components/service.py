import re
import random
from ..utils import format_next
from ..units import unit_update_next, add_unit


class NoAttendantAvailable(Exception):
    pass


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


def update_attendants(attendants, clock):
    _attendants = attendants.copy()
    for attendant in _attendants:
        try:
            if attendant["available_at"] <= clock:
                del attendant["available_at"]
        except KeyError:
            pass

    return _attendants


def get_avaiable_attendant(attendants):
    _attendants = attendants.copy()
    random.shuffle(_attendants)

    selected_attendant = None
    for attendant in _attendants:
        try:
            attendant["available_at"]
        except KeyError:
            selected_attendant = attendant
            break

    if not selected_attendant:
        raise NoAttendantAvailable()

    return _attendants[0]


def process_service_free_attendant(simulation, unit):
    _simulation = simulation.copy()
    component = _simulation["services"][unit["next"]["id"]]
    component["attendants"] = update_attendants(component["attendants"], _simulation["clock"])

    try:
        unit = component["queue"][0]
        del component["queue"][0]
        return process_service_schedule(_simulation, unit)
    except (IndexError, KeyError):
        pass

    return _simulation


def process_service_schedule(simulation, unit):
    _simulation = simulation.copy()
    _unit = unit.copy()
    component = _simulation["services"][_unit["next"]["id"]]
    clock = _simulation["clock"]

    attendants = update_attendants(
        component["attendants"], clock)

    try:
        attendant = get_avaiable_attendant(attendants)
        interval = random.randint(attendant["min"], attendant["max"])

        when = interval + clock
        if when > _simulation["clock_limit"]:
            _simulation["clock_limit"] = when

        attendant["available_at"] = when
        component["attendants"] = [
            a if a["id"] != attendant["id"] else attendant for a in attendants
        ]

        _unit = unit_update_next(_unit, component["next"], clock)
        _simulation["events"] = add_unit(_simulation["events"], _unit, when)
        _simulation["events"] = add_unit(_simulation["events"], {
            "next": {
                "type": 'service',
                "id": component["id"],
                "action": "free_attendant",
                "attendant": attendant
            }
        }, when)
    except NoAttendantAvailable:
        history = {
            "type": "service",
            "action": "queue",
            "id": _unit["next"]["id"]
        }
        try:
            _unit["unit"]["history"][clock].append(history)
        except KeyError:
            _unit["unit"]["history"][clock] = [history]

        try:
            component["queue"].append(_unit)
        except KeyError:
            component["queue"] = [_unit]

    return _simulation


def process_service(simulation, unit):
    try:
        action = unit["next"]["action"]
        if action == "free_attendant":
            return process_service_free_attendant(simulation, unit)
    except KeyError:
        return process_service_schedule(simulation, unit)
