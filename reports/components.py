from .units import get_queues_stats


def get_base_component_info(event, components_instances):
    try:
        stats = components_instances[event["id"]]
        stats["first_entrance"] = min(
            stats["first_entrance"],
            event["at"]
        )
        stats["last_entrance"] = max(
            stats["last_entrance"],
            event["at"]
        )
        stats["attendances"] += 1
        return stats
    except KeyError:
        return {
            "first_entrance": event["at"],
            "last_entrance": event["at"],
            "attendances": 1
        }


def get_entrance_stats(event, components):
    return get_base_component_info(event, components["entrances"])


def get_service_stats(event, components):
    stats = get_base_component_info(event, components["services"])
    try:
        stats["attending_time"] += event["duration"]
    except KeyError:
        stats["attending_time"] = event["duration"]

    return stats


def get_services_queues_stats(units, components):
    _units = units.copy()
    queues = {}
    for unit in _units:
        for queue in get_queues_stats(unit):
            try:
                service_queue = queues[queue["id"]]
                service_queue["total"] += queue["duration"]
                service_queue["amount"] += 1
                service_queue["biggest_waiting_time"] = max(
                    service_queue["biggest_waiting_time"],
                    queue["duration"]
                )
            except KeyError:
                queues[queue["id"]] = {
                    "total": queue["duration"],
                    "amount": 1,
                    "biggest_waiting_time": queue["duration"]
                }

    for id, info in components["services"].items():
        try:
            queue_info = queues[id]
            info["average_waiting_time"] = (
                queue_info["total"] / queue_info["amount"]
            )
            info["probability_of_waiting"] = (
                queue_info["amount"] / info["attendances"]
            )
            info["biggest_waiting_time"] = (
                queue_info["biggest_waiting_time"]
            )
        except KeyError:
            info["average_waiting_time"] = 0
            info["probability_of_waiting"] = 0
            info["biggest_waiting_time"] = 0

        attending_time = info["attending_time"]
        attendances = info["attendances"]
        info["average_service_duration"] = attending_time / attendances
        components["services"][id] = info

    return components["services"]


def get_route_stats(event, components):
    return get_base_component_info(event, components["routes"])


def get_exit_stats(event, components):
    return get_base_component_info(event, components["exits"])


def get_components_base_stats(units):
    _units = units.copy()

    components = {
        "entrances": {},
        "services": {},
        "routes": {},
        "exits": {}
    }

    for unit in _units:
        for event in unit["history"]:
            if event["type"] == "entrance":
                stats = get_entrance_stats(event, components)
                components["entrances"][event["id"]] = stats

            if event["type"] == "service":
                try:
                    if event["action"] == "queue":
                        continue
                except KeyError:
                    pass

                stats = get_service_stats(event, components)
                components["services"][event["id"]] = stats

            if event["type"] == "route":
                stats = get_route_stats(event, components)
                components["routes"][event["id"]] = stats

            if event["type"] == "exit":
                stats = get_exit_stats(event, components)
                components["exits"][event["id"]] = stats

    return components


def get_components_stats(units):
    _units = units.copy()

    components = get_components_base_stats(_units)
    components["services"] = get_services_queues_stats(_units, components)

    return components
