import json
import pathlib
import re
from collections import defaultdict

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
    data = {}
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    rentals = process_rentals(data['rentals'])
    ships = []
    for vehicle in data['vehicles']:
        name = ship_name(vehicle['name'])
        if name is None:
            continue
        if name == 'Retaliator':
            continue
        exported = {
            'source': 'scwiki',
            'name': name,
            'buy_usd': parse_price(vehicle['standalone_cost']),
            'loaners': parse_loaners(vehicle['loaner']),
        }
        if name in rentals:
            rental = rentals[name]
            exported['rent_auec_1day'] = rental['1day'][0]
            exported['rent_auec_3day'] = rental['3day'][0]
            exported['rent_auec_7day'] = rental['7day'][0]
            exported['rent_auec_30day'] = rental['30day'][0]
        ships.append(exported)
    return ships


def process_rentals(rentals):
    ships = {}
    for rental in rentals:
        name = ship_name(rental['ship'])
        if not name in ships:
            ships[name] = {'1day': [], '3day': [], '7day': [], '30day': []}
        ships[name]['1day'].append(integer(rental['1day']))
        ships[name]['3day'].append(integer(rental['3day']))
        ships[name]['7day'].append(integer(rental['7day']))
        ships[name]['30day'].append(integer(rental['30day']))
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
