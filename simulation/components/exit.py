import re
from ..units import unit_update_next, add_unit

exit_regex = r"^S(\d+)$"


def is_exit(str):
    return re.search(exit_regex, str)


def generate_exit(raw):
    groups = re.search(exit_regex, raw).groups()

    return {
        "type": "exit",
        "id": int(groups[0]),
    }


def process_exit(simulation, unit):
    _simulation = simulation.copy()
    _unit = unit_update_next(unit, None, _simulation["clock"])
    _simulation["events"] = add_unit(_simulation["events"], _unit, "done")
    return _simulation
