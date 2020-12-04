import random
from uuid import uuid4
from entities import lines_to_entities
import json

def get_inputs() -> list:
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return lines

def add_unit(events: dict, unit: dict, when) -> dict:
    _events = events.copy()
    try:
        _events[when]
    except KeyError:
        _events[when] = []
    
    _events[when].append(unit)
    return _events

def unit_update_next(unit: dict, next, clock):
    _unit = unit.copy()
    _unit["history"][clock] = {
        "type": _unit["next"]["type"],
        "id": _unit["next"]["id"]
    }
    if next:
        _unit["next"] = {
            "type": next["type"],
            "id": next["id"]
        }
    else:
        del _unit["next"]
    return _unit

"""
Convert events to unit this with a history and when they exit add that in the history_list
"""

# TODO: Handle invalid ID
def handle_next_event(simulation, units, unit: dict, clock: int) -> dict:
    _unit = unit.copy()
    _units = units.copy()

    if (_unit["next"]["type"] == "service"):
        component = simulation["services"][_unit["next"]["id"]]
        interval = random.randint(component["attendants"][0]["min"], component["attendants"][0]["max"])
        when = interval + clock
        _unit = unit_update_next(unit, component["next"], clock)
        _units = add_unit(_units, _unit, when)
        return _units, when

    if (_unit["next"]["type"] == "exit"):
        _unit = unit_update_next(unit, None, clock)
        _units = add_unit(_units, _unit, "done")

    return _units, clock
    

def run_entrances(simulation, units: dict) -> dict:
    _units = units.copy()
    clock = 1
    clock_limit = list(_units.keys()).pop()

    while clock <= clock_limit:
        while True:
            try:
                unit = _units[clock].pop()
                _units, when = handle_next_event(simulation, _units, unit, clock)
                clock_limit = when if when > clock_limit else clock_limit
            except:
                break;

        clock += 1

    return _units["done"]

def generete_entrances(entrances, duration):
    events = {}

    for entrance in entrances.values():
        entrance_duration = 1
        while entrance_duration <= duration:
            interval = random.randint(entrance["min"], entrance["max"])
            unit = {
                "id": str(uuid4()),
                "next": entrance["next"],
                "history": {
                    entrance_duration: {
                        "type": entrance["type"],
                        "id": entrance["id"],
                    }
                }
            }
            events = add_unit(events, unit, entrance_duration)
            entrance_duration += interval

    return events

def run_simulation(inputs: list = []):
    simulation = lines_to_entities(inputs)

    units = generete_entrances(simulation["entrances"], simulation["duration"]["value"])

    finished_units = run_entrances(simulation, units)
    print("---- finished -----")
    print(json.dumps(finished_units, indent=True))
    
run_simulation(get_inputs())