import re

entities_models = {
    "entrance": {
        "regex": r"^G(\d):(\d+)-(\d+);([CRS]\d+)$"
    },
    "proccess": {
        "regex": r"^C(\d);(\d+);((\d+:\d+-\d+,?)+);([CRS]\d+)$"
    },
    "route": {
        "regex": r"^R(\d);((0,\d+-[CSR]\d+;?)+)$"
    },
    "exit": {
        "regex": r"^S(\d+)$"
    },
    "duration": {
        "regex": r"^TS=(\d+)$"
    }
}

def line_to_entity(line: str) -> dict:
    for type, data in  entities_models.items():
        if re.search(data["regex"], line):
            return type

def lines_to_entities(inputs: list = []) -> dict:
    for input in inputs:
        print(line_to_entity(input))