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
