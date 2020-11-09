import random
from uuid import uuid4
from entities import lines_to_entities

def get_inputs() -> list:
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return lines


def add_event(events: dict, event: dict, duration: int) -> dict:
    fresh_events = events.copy()
    try:
        fresh_events[duration]
    except KeyError:
        fresh_events[duration] = []
    
    fresh_events[duration].append(event)
    return fresh_events

"""
Convert events to unit this with a history and when they exit add that in the history_list
"""

def generate_next_event(simulation, event: dict) -> dict:
    pass

def run_entrances(simulation, events: dict, duration: int) -> dict:
    fresh_events = events.copy()
    history_events = {}
    clock = 1
    clock_limit = list(events.keys()).pop()

    while clock <= clock_limit:
        while True:
            try:
                entity = fresh_events[clock].pop()
                history_events = add_event(history_events, entity, duration)
                generate_next_event(simulation, entity)
            except:
                break;

        clock += 1

    return history_events

def run_simulation(inputs: list = []):
    events = {}
    units = {}
    simulation = lines_to_entities(inputs)

    print(simulation)

    duration = simulation["duration"]["value"]

    print(uuid4())

    for entrance in simulation["entrances"].values():
        entrance_duration = 1
        while entrance_duration <= duration:
            interval = random.randint(entrance["min"], entrance["max"])
            events = add_event(events, entrance, entrance_duration)
            units[uuid4()] = [entrance]
            entrance_duration += interval

    print(units)

    #print(run_entrances(simulation, events, duration))
    
run_simulation(get_inputs())