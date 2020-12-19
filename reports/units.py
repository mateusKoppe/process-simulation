def get_queues_stats(unit):
    history = unit["history"].copy()
    events_time = list(map(lambda x: int(x), history.keys()))
    queues = []
    for time, events in history.items():
        for event in events:
            try:
                if (event["action"] == "queue"):
                    queues.append({
                        "type": event["type"],
                        "id": event["id"],
                        "at": int(time)
                    })
            except KeyError:
                pass

    for queue in queues:
        time_index = events_time.index(queue["at"])
        finished_time = events_time[time_index + 1]
        queue["duration"] = finished_time - queue["at"]

    return queues


def get_unit_stats(unit):
    history = unit["history"].copy()
    events_time = list(map(lambda x: int(x), history.keys()))
    entrance_time = events_time[0]
    exit_time = events_time[len(events_time) - 1]
    time_spent = exit_time - entrance_time

    queues = get_queues_stats(unit)
    time_in_queue = 0
    for queue in queues:
        time_in_queue += queue["duration"]

    return {
        "time_spent": time_spent,
        "time_in_queue": time_in_queue,
        "queues": queues
    }


def get_units_stats(units):
    return list(map(get_unit_stats, units))
