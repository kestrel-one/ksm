import json
import pathlib

from fields.ships import (
    ship_name,
    ship_size,
)
from fields.types import (
    decimal,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def export():
    items = []
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)
    ships = []
    for item in items:
        name = ship_name(item['displayName'])
        if name is None:
            continue
        ships.append({
            'source': 'hardpoint',
            'name': name,
            'size': ship_size(item['size'], name),
            'mass': decimal(item['mass']),
            'buy_auec': decimal(item.get('basePrice'), True),
        })
    return ships


if __name__ == '__main__':
    export()
