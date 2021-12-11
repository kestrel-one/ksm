import json
import pathlib
import re

from fields.ships import (
    ship_name,
    ship_size,
)
from fields.types import (
    decimal,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'

RE_PORT_WEAPON_NAME = re.compile(r'^(turret_|hardpoint_(turret|weapon))')

WEAPON_PREFIX_ALLOWED = [
    'turret',
    'hardpoint_turret',
    'hardpoint_weapon_class2_',
    'hardpoint_weapon_s02_',
    'hardpoint_weapon_gun_',
    'hardpoint_weapon_missile_',
    'hardpoint_weapon_missilebay_',
    'hardpoint_weapon_missilerack_',
    'hardpoint_weapon_spine',
    'hardpoint_weapon_nose',
    'hardpoint_weapon_wing_',
    'hardpoint_weapon_left',
    'hardpoint_weapon_right',
    'hardpoint_weapon_center',
    'hardpoint_weapon_centre',
    'hardpoint_weapon_front_',
    'hardpoint_weapon_top',
    'hardpoint_weapon_bottom',
]

WEAPON_PREFIX_IGNORED = [
    'hardpoint_weapon_emp',
    'hardpoint_weapon_locker_',
    'hardpoint_weapon_missilelauncher',
    'hardpoint_weapon_missilelauncher_',
    'hardpoint_weapon_rack',
    'hardpoint_weapon_regen_',
]


def export():
    items = []
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)
    ships = []
    for item in items:
        name = ship_name(item['displayName'])
        if name is None:
            continue
        turrets = find_turrets(item)
        guns = find_guns(item)
        missiles = find_missiles(item)
        ships.append({
            'source': 'hardpoint',
            'name': name,
            'size': ship_size(item['size'], name),
            'mass': decimal(item['mass']),
            'num_weapons': len(guns) + len(turrets) + len(missiles),
            'num_guns': len(guns),
            'num_turrets': len(turrets),
            'num_missiles': len(missiles),
            'guns': guns,
            'turrets': turrets,
            'missiles': missiles,
            'buy_auec': decimal(item.get('basePrice'), True),
        })
    return ships


def find_guns(item):
    guns = []
    for port in item['ports']:
        if not is_weapon_port(port):
            continue
        types = [t['type'] for t in port['types']]
        if 'WeaponGun' in types:
            guns.append(port['maxSize'])
    return guns


def find_turrets(item):
    turrets = []
    for port in item['ports']:
        if not is_weapon_port(port):
            continue
        types = [t['type'] for t in port['types']]
        subtypes = [t['subtype'] for t in port['types']]
        if 'TurretBase' in types and 'MannedTurret' in subtypes:
            turrets.append(port['maxSize'])
    return turrets


def find_missiles(item):
    missiles = []
    for port in item['ports']:
        if not is_weapon_port(port):
            continue
        types = [t['type'] for t in port['types']]
        if 'MissileLauncher' in types:
            missiles.append(port['maxSize'])
    return missiles


def is_weapon_port(port):
    name = port['name']
    if not RE_PORT_WEAPON_NAME.match(name):
        return False
    should_allow = has_prefix(name, WEAPON_PREFIX_ALLOWED)
    should_ignore = has_prefix(name, WEAPON_PREFIX_IGNORED)
    if not should_allow and not should_ignore:
        raise ValueError('Unexpected weapon name: ' + name)
    if should_ignore:
        return False
    return True


def has_prefix(name, prefixes):
    return any([name.startswith(prefix) for prefix in prefixes])


if __name__ == '__main__':
    export()
