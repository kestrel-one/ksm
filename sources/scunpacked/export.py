import json
import math
import pathlib

from collections import defaultdict

from fields.ships import (
    flatten_objects,
    ship_cargo,
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
    ship_rental_pct = defaultdict(lambda: defaultdict(list))
    for shop in shops:
        for inventory in shop['inventory']:
            type_ = inventory.get('type')
            name = inventory.get('name')
            displayName = inventory.get('displayName')
            if name == 'drak_cutlass_red_update':
                displayName = 'Drake Cutlass Red'
                type_ = 'NOITEM_Vehicle'
            elif name == 'drak_cutlass_blue_update':
                displayName = 'Drake Cutlass Blue'
                type_ = 'NOITEM_Vehicle'
            elif type_ != 'NOITEM_Vehicle':
                continue
            if inventory['shopSellsThis']:
                ship_prices[ship_name(displayName)].append(inventory['basePrice'])
            if inventory['shopRentThis']:
                for rental_template in inventory['rentalTemplates']:
                    pct = float(rental_template['PercentageOfSalePrice'])
                    if pct > 0:
                        ship_rental_pct[ship_name(displayName)][rental_template['RentalDuration']].append(pct)
    for ship, prices in ship_prices.items():
        if prices.count(prices[0]) != len(prices):
            raise ValueError('Uh oh! Base prices dont match for ship: %s' % ship)
        ship_prices[ship] = prices[0]
    ship_rentals = defaultdict(lambda: defaultdict(dict))
    for ship, days in ship_rental_pct.items():
        ship_price = ship_prices[ship]
        for day, pcts in days.items():
            if not all(pct == pcts[0] for pct in pcts):
                raise ValueError('Rental pct mismatch: %s (%s)' % (ship, pcts))
            ship_rentals[ship][day] = math.ceil((pcts[0] * ship_price * day)/100)
    for ship, days in ship_rentals.items():
        ship_rentals[ship] = dict(days)
    ship_rentals = dict(ship_rentals)

    exported_ships = []
    for _, item in ships.items():
        base_name = item['ship']['Name']
        class_name = item['ship']['ClassName']
        if '_BIS' in class_name:
            continue
        if class_name.endswith('_Modifiers') or class_name.startswith('TEST_') or class_name.endswith('_FW22NFZ') or class_name.endswith('_SM_TE') or class_name.endswith('_Bombless'):
            # Not sure what these are but they were creating duplicate ships
            continue
        if class_name == 'AEGS_Idris_Distance_Destruction':
            continue
        name = ship_name(base_name)
        if name == 'Retaliator':
            name = 'Retaliator Bomber'
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
            'cargo': ship_cargo(item, name),
            'max_speed': decimal(item['ship']['FlightCharacteristics']['MaxSpeed']),
            'scm_speed': decimal(item['ship']['FlightCharacteristics']['ScmSpeed']),
            'qt_speed': integer(int(item['ship']['QuantumTravel']['Speed'] / 1000)),

            'has_quantum_drive': decimal(item['ship']['QuantumTravel']['Speed']) > 0,
            'has_gravlev': item['ship'].get('IsGravlev', False),

            'ins_std_claim_time': minutes(item['ship'].get('Insurance', {}).get('StandardClaimTime'), True),
            'ins_exp_claim_time': minutes(item['ship'].get('Insurance', {}).get('ExpeditedClaimTime'), True),
            'ins_exp_cost': integer(item['ship'].get('Insurance', {}).get('ExpeditedCost'), True),
        }
        if name in ship_prices:
            exported_ship['buy_auec'] = math.ceil(ship_prices[name])
        if name in ship_rentals:
            rental = ship_rentals[name]
            exported_ship['rent_auec_1day'] = rental[1]
            exported_ship['rent_auec_3day'] = rental[3]
            exported_ship['rent_auec_7day'] = rental[7]
            exported_ship['rent_auec_30day'] = rental[30]
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
