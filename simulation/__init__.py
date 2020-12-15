from .components.entrance import generate_entrance, is_entrance
from .components.service import generate_service, is_service, process_service
from .components.exit import generate_exit, is_exit, process_exit
from .components.route import generate_route, is_route, process_route
from .components.duration import duration_generate, is_duration
from .units import generete_entrances
import json

entities_models = {
    "entrance": {
        "is": is_entrance,
        "generate": generate_entrance,
    },
    "service": {
        "is": is_service,
        "generate": generate_service,
    },
    "route": {
        "is": is_route,
        "generate": generate_route,
    },
    "exit": {
        "is": is_exit,
        "generate": generate_exit,
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


def handle_next_event(simulation, unit):
    _simulation = simulation.copy()
    _unit = unit.copy()

    if (_unit["next"]["type"] == "service"):
        _simulation = process_service(_simulation, _unit)

    if (_unit["next"]["type"] == "route"):
        _simulation = process_route(_simulation, _unit)

    if (_unit["next"]["type"] == "exit"):
        _simulation = process_exit(_simulation, _unit)

    return _simulation


def run_entrances(simulation):
    _simulation = simulation.copy()
    units = _simulation["events"].copy()
    _simulation["clock"] = 1
    _simulation["clock_limit"] = list(units.keys()).pop()

    while _simulation["clock"] <= _simulation["clock_limit"]:
        while True:
            try:
                unit = _simulation["events"][_simulation["clock"]].pop()
                _simulation = handle_next_event(_simulation, unit)
            except (KeyError, IndexError):
                break

        _simulation["clock"] += 1

    return _simulation["events"]["done"]


def run_simulation(inputs=[]):
    simulation = lines_to_entities(inputs)

    simulation["events"] = generete_entrances(simulation)

    finished_units = run_entrances(simulation)
    print("---- finished -----")
    print(json.dumps(finished_units, indent=True))
