import json
import pathlib

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def export():
    items = []
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)['data']
    ships = []
    for item in items:
        pass
    return ships


if __name__ == '__main__':
    export()
