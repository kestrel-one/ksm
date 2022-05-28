import json
import pathlib

from fields.ships import (
    ship_crew_range,
    ship_name,
    ship_url,
)
from fields.types import (
    integer,
)

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def min_price(sales):
    if sales is None:
        return None
    return min(integer(sale['price']) for sale in sales)


def export():
    items = []
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)['data']
    ships = []
    for item in items:
        name = ship_name(item['name'])
        if name is None:
            continue
        min_crew, max_crew = ship_crew_range(item['crew'])
        url = None
        if item['store_url']:
            url = ship_url(item['store_url'])
        ship = {
            'source': 'uex',
            'name': name,
            'buy_auec': min_price(item['buy_at']),
            'rent_auec': min_price(item['rent_at']),
            'url': url,
        }
        if item['price']:
            ship['buy_usd'] = integer(item['price'])
        ships.append(ship)
    return ships


if __name__ == '__main__':
    export()
