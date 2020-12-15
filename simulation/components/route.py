import re
import random
from ..utils import format_next
from ..units import unit_update_next, add_unit

route_regex = r"^R(\d);((0.\d+-[CSR]\d+;?)+)$"


def is_route(str):
    return re.search(route_regex, str)


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


def process_route(simulation, units, unit, clock):
    component = simulation["routes"][unit["next"]["id"]]

    sum = 0
    for route in component["routes"]:
        sum += route["percentage"]

    pick_value = random.random() * sum
    percentage_acc = 0
    selected_route = None
    for route in component["routes"]:
        percentage_acc += route["percentage"]
        if pick_value <= percentage_acc:
            selected_route = route
            break

    _unit = unit_update_next(unit, selected_route["next"], clock)
    _units = add_unit(units, _unit, clock)
    return _units, clock
