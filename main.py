from simulation import run_simulation
from reports import get_units_stats, get_components_stats
import json


def get_inputs():
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return lines


simulation_result = run_simulation(get_inputs())
print(json.dumps({
    "unitsFlow": simulation_result,
    "unitsStats": get_units_stats(simulation_result),
    "componentStats": get_components_stats(simulation_result)
}, indent=True))
