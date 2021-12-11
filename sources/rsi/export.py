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
        if ship is not None:
            ships.append(ship)
    return ships


def item_to_ship(item):
    name = ship_name(item['name'])
    if name is None:
        return None
    return {
        'source': 'rsi',
        'id': integer(item['id']),
        'name': name,
        'status': ship_status(item['production_status']),
        'url': ship_url(item['url']),
        'size': ship_size(item['size'], name),
        'manufacturer_name': ship_manu_name(item['manufacturer']['name']),
        'manufacturer_code': ship_manu_code(item['manufacturer']['code']),
        'mass': decimal(item['mass'], True),
        'height': decimal(item['height'], True),
        'length': decimal(item['length'], True),
        'beam': decimal(item['beam'], True),
        'cargo': integer(item['cargocapacity'], True),
        'min_crew': integer(item['min_crew'], True),
        'max_crew': integer(item['max_crew'], True),
        'max_speed': decimal(item['afterburner_speed'], True),
        'scm_speed': decimal(item['scm_speed'], True),
        'has_quantum_drive': has_quantum_drive(item),
        'num_weapons': mount_count(item),
        'num_guns': mount_count(item, 'weapons'),
        'num_turrets': mount_count(item, 'turrets'),
        'num_missiles': mount_count(item, 'missiles'),
        'guns': mount_sizes(item, 'weapons'),
        'turrets': mount_sizes(item, 'turrets'),
        'missiles': mount_sizes(item, 'missiles'),
    }


def has_quantum_drive(item):
    drives = item \
        .get('compiled', {}) \
        .get('RSIPropulsion', {}) \
        .get('quantum_drives', [])
    return len(drives) > 0


def mount_count(item, groupFilter=None):
    mounts = __mounts(item, groupFilter)
    return sum([mount['count'] for mount in mounts])


def mount_sizes(item, groupFilter=None):
    sizes = []
    for mount in __mounts(item, groupFilter):
        for _ in range(mount['count']):
            sizes.append(mount['size'])
    sizes.sort()
    return sizes


def __mounts(item, groupFilter=None):
    groups = ('weapons', 'turrets', 'missiles')
    item = item.get('compiled', {}).get('RSIWeapon', {})
    mounts = []
    for group in groups:
        if groupFilter is not None and group != groupFilter:
            continue
        for mount in item.get(group, []):
            count = int(mount['mounts'])
            mounts.append({'size': __mount_size(mount), 'count': count})
    return mounts


def __mount_size(mount):
    value = mount.get('size', '-')
    if value == '-':
        value = 0
    size = int(value)
    if size < 0 or size > 12:
        raise ValueError('Unknown mount size: %s', size)
    return size


if __name__ == '__main__':
    export()
