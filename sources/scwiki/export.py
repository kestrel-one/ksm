import json
import pathlib
import re

from fields.ships import (
    ship_name,
)
from fields.types import (
    integer,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'
COL_NAMES = ['name', 'price']
RE_PRICE = re.compile('[^0-9\.]')


def export():
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)
    ships = []
    for item in items:
        name = ship_name(item['name'])
        if name is None:
            continue
        ships.append({
            'source': 'scwiki',
            'name': name,
            'buy_usd': parse_price(item['standalone_cost']),
            'loaners': parse_loaners(item['loaner']),
        })
    return ships


def parse_price(text):
    if '(' in text:
        text = text.split('(')[0]
    price = RE_PRICE.sub('', text)
    price = integer(price) if price else None
    return price


def parse_loaners(text):
    if text == '-' or text == '—':
        return []
    loaners = []
    for name in text.split(','):
        name = ship_name(name)
        loaners.append(name)
    return loaners


if __name__ == '__main__':
    export()
