def get_queues_stats(unit):
    history = unit["history"].copy()
    queues = []
    for event in history:
        try:
            if (event["action"] != "queue"):
                next

            queues.append({
                "type": event["type"],
                "id": event["id"],
                "at": event["at"],
                "duration": event["duration"]
            })
        except KeyError:
            pass

    return queues


def get_unit_stats(unit):
    history = unit["history"].copy()
    entrance_time = history[0]["at"]
    exit_time = history[len(history) - 1]["at"]
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
