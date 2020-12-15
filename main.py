from simulation import run_simulation


def get_inputs():
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return lines


run_simulation(get_inputs())
