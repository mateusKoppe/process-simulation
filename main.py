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


def run_simulation(inputs: list = []):
    simulation = lines_to_entities(inputs)
    
run_simulation(get_inputs())