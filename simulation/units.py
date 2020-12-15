import random
from uuid import uuid4


def add_unit(events, unit, when):
    _events = events.copy()
    try:
        _events[when]
    except KeyError:
        _events[when] = []

    _events[when].append(unit)
    return _events


def unit_update_next(unit, next, clock):
    _unit = unit.copy()

    try:
        _unit["history"][clock]
    except KeyError:
        _unit["history"][clock] = []

    _unit["history"][clock].append({
        "type": _unit["next"]["type"],
        "id": _unit["next"]["id"]
    })
    if next:
        _unit["next"] = {
            "type": next["type"],
            "id": next["id"]
        }
    else:
        del _unit["next"]
    return _unit


def generete_entrances(simulation):
    duration = simulation["duration"]["value"]
    entrances = simulation["entrances"]
    events = {}

    for entrance in entrances.values():
        entrance_duration = 1
        while entrance_duration <= duration:
            interval = random.randint(entrance["min"], entrance["max"])
            unit = {
                "id": str(uuid4()),
                "next": entrance["next"],
                "history": {
                    entrance_duration: [{
                        "type": entrance["type"],
                        "id": entrance["id"],
                    }]
                }
            }
            events = add_unit(events, unit, entrance_duration)
            entrance_duration += interval

    return events
