import json
import pathlib

from collections import defaultdict

from fields.ships import (
    ship_manu_code,
    ship_manu_name,
    ship_name,
    ship_size,
)
from fields.types import (
    decimal,
    integer,
    minutes,
)

SHIPS_DATA_PATH = pathlib.Path(__file__).parent / 'ships.json'
SHOPS_DATA_PATH = pathlib.Path(__file__).parent / 'shops.json'


def export():
    ships = []
    with open(SHIPS_DATA_PATH, 'r') as f:
        ships = json.load(f)
    shops = []
    with open(SHOPS_DATA_PATH, 'r') as f:
        shops = json.load(f)

    ship_prices = defaultdict(list)
    for shop in shops:
        for inventory in shop['inventory']:
            if inventory.get('type') != 'NOITEM_Vehicle':
                continue
            if not inventory['shopSellsThis']:
                continue
            ship_prices[inventory['displayName']].append(inventory['basePrice'])
    for ship, prices in ship_prices.items():
        if prices.count(prices[0]) != len(prices):
            raise ValueError('Uh oh! Base prices dont match for ship: %s' % ship)
        ship_prices[ship] = prices[0]

    exported_ships = []
    for _, item in ships.items():
        base_name = item['ship']['Name']
        class_name = item['ship']['ClassName']
        if '_BIS' in class_name:
            continue
        if class_name.endswith('_Modifiers') or class_name.startswith('TEST_'):
            # Not sure what these are but they were creating duplicate ships
            continue
        name = ship_name(base_name)
        if name is None:
            continue
        fix_vehicle_size(item)
        exported_ship = {
            'source': 'scunpacked',
            'name': name,
            'size': ship_size(item['ship']['Size'], name),
            'manufacturer_name': ship_manu_name(item['ship']['Manufacturer']['Name']),
            'manufacturer_code': ship_manu_code(item['ship']['Manufacturer']['Code']),
            'mass': decimal(item['ship']['Mass']),
            'cargo': integer(item['ship']['Cargo']),
            'max_speed': decimal(item['ship']['FlightCharacteristics']['MaxSpeed']),
            'scm_speed': decimal(item['ship']['FlightCharacteristics']['ScmSpeed']),
            'qt_speed': integer(int(item['ship']['QuantumTravel']['Speed'] / 1000)),

            'has_quantum_drive': decimal(item['ship']['QuantumTravel']['Speed']) > 0,
            'has_gravlev': item['ship'].get('IsGravlev', False),

            'ins_std_claim_time': minutes(item['ship'].get('Insurance', {}).get('StandardClaimTime'), True),
            'ins_exp_claim_time': minutes(item['ship'].get('Insurance', {}).get('ExpeditedClaimTime'), True),
            'ins_exp_cost': integer(item['ship'].get('Insurance', {}).get('ExpeditedCost'), True),
        }
        if base_name in ship_prices:
            exported_ship['buy_auec'] = int(ship_prices.get(base_name))
        exported_ships.append(exported_ship)
    return exported_ships


def fix_vehicle_size(item):
    if item['ship'].get('IsVehicle', False):
        item['ship']['Size'] = 'Vehicle'


if __name__ == '__main__':
    export()

# Command for digging into exported JSON:
# cat sources/scunpacked/ships.json | jq '[ .[] | select(.ship.Name|contains("C2")) ][]'
# cat sources/scunpacked/ships.json | jq '[ .[] | select(.ship.Name|contains("C2")) ][] | {ship}[] | {Name,ClassName,Role,Size,Cargo,Crew,Mass,IsSpaceship}'
# cat sources/scunpacked/shops.json | jq '.[] | .inventory[] | select(.displayName != null) | select(.displayName|contains("Avenger Stalker"))'
