import csv
import pathlib

from fields.ships import (
    ship_name,
)
from fields.types import (
    decimal,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.csv'
COL_NAMES = [
    'ship_name',
    'last_update',
    'updated_by',
    'patch',
    'notes',
    'accel_fwd',
    'accel_fwd_boost',
    'accel_back',
    'accel_back_boost',
    'accel_up',
    'accel_up_boost',
    'accel_down',
    'accel_down_boost',
    'accel_left',
    'accel_left_boost',
    'accel_right',
    'accel_right_boost',
    'rotv_pitch',
    'rotv_yaw',
    'rotv_roll',
    'boost_idle',
    'boost_fwd',
    'gun_score',
    'missile_score',
    'shield_score',
    'scm_speed',
    'cruise_speed',
    'durability_nose',
]


def export():
    ships = []
    for item in create_items():
        name = ship_name(item['ship_name'])
        if name is None:
            continue
        ships.append({
            'source': 'spat',
            'name': name,
            'scm_speed': decimal(item['scm_speed']),
            'max_speed': decimal(item['cruise_speed']),
        })
    return ships


def create_items():
    rows = []
    with open(DATA_PATH, 'r') as f:
        rows = list(csv.reader(f))[1:]
    items = []
    max_col = len(COL_NAMES)
    for i, row in enumerate(rows):
        item = {}
        for j, col in enumerate(row):
            if j < max_col:
                item[COL_NAMES[j]] = col
        items.append(item)
    return items


if __name__ == '__main__':
    export()
