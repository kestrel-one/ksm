import json
import pathlib

from fields.ships import (
    ship_manu_code,
    ship_manu_name,
    ship_name,
    ship_size,
    ship_status,
    ship_url,
)
from fields.types import (
    decimal,
    integer,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def export():
    items = []
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)['data']
    ships = []
    for item in items:
        ship = item_to_ship(item)
        if ship is None:
            continue
        if ship['name'] == 'Retaliator':
            continue
        ships.append(ship)
    return ships


def item_to_ship(item):
    name = ship_name(item['name'])
    if name is None:
        return None
    maxc = integer(item['max_crew'], True)
    minc = integer(item['min_crew'], True) or maxc
    status = ship_status(item['production_status'])
    return {
        'source': 'rsi',
        'id': integer(item['id']),
        'name': name,
        'status': status,
        'url': ship_url(item['url']),
        'size': ship_size(item['size'], name),
        'manufacturer_name': ship_manu_name(item['manufacturer']['name']),
        'manufacturer_code': ship_manu_code(item['manufacturer']['code']),
        'mass': decimal(item['mass'], True),
        'height': decimal(item['height'], True),
        'length': decimal(item['length'], True),
        'beam': decimal(item['beam'], True),
        'cargo': integer(item['cargocapacity'], True),
        'min_crew': minc,
        'max_crew': maxc,
        'max_speed': decimal(item['afterburner_speed'], True),
        'scm_speed': decimal(item['scm_speed'], True),
        'has_quantum_drive': has_quantum_drive(item),
    }


def has_quantum_drive(item):
    drives = item \
        .get('compiled', {}) \
        .get('RSIPropulsion', {}) \
        .get('quantum_drives', [])
    return len(drives) > 0


if __name__ == '__main__':
    export()
