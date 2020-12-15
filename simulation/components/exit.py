import re
from ..units import unit_update_next, add_unit

exit_regex = r"^S(\d+)$"


def is_exit(str):
    return re.search(exit_regex, str)


def exit_generate(raw):
    groups = re.search(exit_regex, raw).groups()

    return {
        "type": "exit",
        "id": int(groups[0]),
    }


def process_exit(simulation, units, unit, clock):
    _unit = unit_update_next(unit, None, clock)
    _units = add_unit(units, _unit, "done")
    return _units, clock
