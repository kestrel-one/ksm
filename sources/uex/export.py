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
    code_to_name = {}
    ships = []
    for item in items:
        name = ship_name(item['name'])
        if name is None:
            continue
        min_crew, max_crew = ship_crew_range(item['crew'])
        ship = {
            'source': 'uex',
            'name': name,
            'buy_auec': min_price(item['buy_at']),
            'rent_auec': min_price(item['rent_at']),
            'url': ship_url(item['store_url']),
            'loaners': (item['loaner'] or '').split(','),
            'min_crew': min_crew,
            'max_crew': max_crew,
        }
        if item['price']:
            ship['buy_usd'] = integer(item['price'])
        ships.append(ship)
        code_to_name[item['code']] = name
    for ship in ships:
        loaners = [code_to_name.get(code) for code in ship['loaners']]
        ship['loaners'] = [loaner for loaner in loaners if loaner]
    return ships


if __name__ == '__main__':
    export()
