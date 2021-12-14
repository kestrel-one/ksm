import json
import pathlib

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

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def export():
    items = []
    with open(DATA_PATH, 'r') as f:
        items = json.load(f)
    ships = []
    for _, item in items.items():
        if '_BIS' in item['ship']['ClassName']:
            continue
        if item['ship']['ClassName'].endswith('_Modifiers'):
            # Not sure what this is but it was creating duplicate ships
            continue
        name = ship_name(item['ship']['Name'])
        if name is None:
            continue
        fix_vehicle_size(item)
        ships.append({
            'source': 'scunpacked',
            'name': name,
            'size': ship_size(item['ship']['Size'], name),
            'manufacturer_name': ship_manu_name(item['ship']['Manufacturer']['Name']),
            'manufacturer_code': ship_manu_code(item['ship']['Manufacturer']['Code']),
            'mass': decimal(item['ship']['Mass']),
            'cargo': integer(item['ship']['Cargo']),
            'max_speed': decimal(item['ship']['FlightCharacteristics']['MaxSpeed']),
            'scm_speed': decimal(item['ship']['FlightCharacteristics']['ScmSpeed']),

            'has_quantum_drive': decimal(item['ship']['QuantumTravel']['Speed']) > 0,
            'has_gravlev': item['ship'].get('IsGravlev', False),

            'ins_std_claim_time': minutes(item['ship'].get('Insurance', {}).get('StandardClaimTime'), True),
            'ins_exp_claim_time': minutes(item['ship'].get('Insurance', {}).get('ExpeditedClaimTime'), True),
            'ins_exp_cost': integer(item['ship'].get('Insurance', {}).get('ExpeditedCost'), True),
        })
    return ships


def fix_vehicle_size(item):
    if item['ship'].get('IsVehicle', False):
        item['ship']['Size'] = 'Vehicle'


if __name__ == '__main__':
    export()

# Command for digging into exported JSON:
# cat sources/scunpacked/data.json | jq '[ .[] | select(.ship.Name|contains("C2")) ][] | {ship}[] | {Name,ClassName,Role,Size,Cargo,Crew,Mass,IsSpaceship}'
