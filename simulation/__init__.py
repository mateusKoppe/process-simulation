from .components.entrance import entrance_generate, is_entrance
from .components.service import service_generate, is_service, process_service
from .components.exit import exit_generate, is_exit, process_exit
from .components.route import route_generate, is_route, process_route
from .components.duration import duration_generate, is_duration
from .units import generete_entrances
import json

entities_models = {
    "entrance": {
        "is": is_entrance,
        "generate": entrance_generate,
    },
    "service": {
        "is": is_service,
        "generate": service_generate,
    },
    "route": {
        "is": is_route,
        "generate": route_generate,
    },
    "exit": {
        "is": is_exit,
        "generate": exit_generate,
    },
    "duration": {
        "is": is_duration,
        "generate": duration_generate,
    }
}


def line_to_entity(line):
    for data in entities_models.values():
        if data["is"](line):
            return data["generate"](line)


def lines_to_entities(lines=[]):
    entities = {
        "entrances": {},
        "services": {},
        "routes": {},
        "exits": {},
        "duration": None
    }
    types_to_keys = {
        "entrance": "entrances",
        "service": "services",
        "route": "routes",
        "exit": "exits",
    }
    for line in lines:
        entity = line_to_entity(line)

        try:
            key = types_to_keys[entity["type"]]
            entities[key][entity["id"]] = entity
        except KeyError:
            if entity["type"] == "duration":
                entities["duration"] = entity

    return entities


"""
Convert events to unit this with a history and when they exit add that in the history_list
"""

# TODO: Handle invalid ID


def handle_next_event(simulation, units, unit, clock):
    _unit = unit.copy()
    _units = units.copy()

    if (_unit["next"]["type"] == "service"):
        _units, clock = process_service(simulation, _units, _unit, clock)

    if (_unit["next"]["type"] == "route"):
        _units, clock = process_route(simulation, _units, _unit, clock)

    if (_unit["next"]["type"] == "exit"):
        _units, clock = process_exit(simulation, _units, _unit, clock)

    return _units, clock


def run_entrances(simulation, units):
    _units = units.copy()
    clock = 1
    clock_limit = list(_units.keys()).pop()

    while clock <= clock_limit:
        while True:
            try:
                unit = _units[clock].pop()
                _units, when = handle_next_event(
                    simulation, _units, unit, clock)
                clock_limit = when if when > clock_limit else clock_limit
            except:
                break

        clock += 1

    return _units["done"]


def run_simulation(inputs=[]):
    simulation = lines_to_entities(inputs)

    units = generete_entrances(simulation)

    finished_units = run_entrances(simulation, units)
    print("---- finished -----")
    print(json.dumps(finished_units, indent=True))
