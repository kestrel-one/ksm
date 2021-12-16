import csv
import pathlib
import re

from fields.ships import (
    ship_name,
)
from fields.types import (
    integer,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.csv'
COL_NAMES = ['name', 'price']
RE_PRICE = re.compile('[$,]')


def export():
    ships = []
    for item in create_items():
        name = ship_name(item['name'])
        if name is None:
            continue
        ships.append({
            'source': 'prices',
            'name': name,
            'buy_usd': integer(RE_PRICE.sub('', item['price'])),
        })
    return ships


def create_items():
    rows = []
    with open(DATA_PATH, 'r') as f:
        rows = list(csv.reader(f))[1:]
    items = []
    max_col = len(COL_NAMES)
    for i, row in enumerate(rows):
        item = {'source': 'prices'}
        for j, col in enumerate(row):
            if j < max_col:
                item[COL_NAMES[j]] = col
        items.append(item)
    return items


if __name__ == '__main__':
    export()
