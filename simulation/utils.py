def format_next(next):
    type_table = {
        "G": "entrance",
        "C": "service",
        "R": "route",
        "S": "exit"
    }

    for key, description in type_table.items():
        if (next.startswith(key)):
            return {
                "type": description,
                "id": int(next[1:])
            }

    raise Exception("Invalid next")


def format_events(history):
    _history = history.copy()
    formated_events = []
    for time, events in _history.items():
        for event in events:
            event["at"] = int(time)
            formated_events.append(event)

    for i, event in enumerate(formated_events):
        try:
            next_event = formated_events[i + 1]
            event["duration"] = next_event["at"] - event["at"]
        except IndexError:
            pass

    return formated_events
