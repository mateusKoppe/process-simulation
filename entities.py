import re

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

entrance_regex = r"^G(\d):(\d+)-(\d+);([CRS]\d+)$"
def entrance_generate(raw):
    groups = re.search(entrance_regex, raw).groups()
    return {
        "type": "entrance",
        "id": int(groups[0]),
        "min": int(groups[1]),
        "max": int(groups[2]),
        "next": format_next(groups[3]),
    }

service_regex = r"^C(\d);(\d+);((\d+:\d+-\d+,?)+);([CRS]\d+)$"
def service_generate(raw):
    groups = re.search(service_regex, raw).groups()

    services_raw = groups[2].split(',')

    attendants = []
    for service_raw in services_raw:
        service_groups = re.search(r"^(\d+):(\d+)-(\d+)$", service_raw).groups()
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

route_regex = r"^R(\d);((0.\d+-[CSR]\d+;?)+)$"
def route_generate(raw):
    groups = re.search(route_regex, raw).groups()
    
    routes_raw = groups[1].split(';')
    routes = []
    for route_raw in routes_raw:
        route_groups = re.search(r"^(0.\d+)-([CRS]\d+)", route_raw).groups()
        routes.append({
            "percentage": float(route_groups[0]),
            "next": format_next(route_groups[1]),
        })

    return {
        "type": "route",
        "id": int(groups[0]),
        "routes": routes,
    }

exit_regex = r"^S(\d+)$"
def exit_generate(raw):
    groups = re.search(exit_regex, raw).groups()

    return {
        "type": "exit",
        "id": int(groups[0]),
    }

duration_regex = r"^TS=(\d+)$"
def duration_generate(raw):
    groups = re.search(duration_regex, raw).groups()
    
    return {
        "type": "duration",
        "value": int(groups[0]),
    }

entities_models = {
    "entrance": {
        "regex": entrance_regex,
        "generate": entrance_generate,
    },
    "service": {
        "regex": service_regex,
        "generate": service_generate,
    },
    "route": {
        "regex": route_regex,
        "generate": route_generate,
    },
    "exit": {
        "regex": exit_regex,
        "generate": exit_generate,
    },
    "duration": {
        "regex": duration_regex,
        "generate": duration_generate,
    }
}

def line_to_entity(line):
    for data in entities_models.values():
        if re.search(data["regex"], line):
            return data["generate"](line)

def lines_to_entities(lines = []):
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
        "route":"routes",
        "exit":"exits",
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