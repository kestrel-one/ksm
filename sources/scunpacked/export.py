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
        name = ship_name(item['ship']['Name'])
        if name is None:
            continue
        fix_vehicle_size(item)
        guns = find_guns(item)
        turrets = find_turrets(item)
        missiles = find_missiles(item)
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

            'num_weapons': len(turrets) + len(guns) + len(missiles),
            'num_guns': len(guns),
            'num_turrets': len(turrets),
            'num_missiles': len(missiles),
            'guns': guns,
            'turrets': turrets,
            'missiles': missiles,

            'ins_std_claim_time': minutes(item['ship'].get('Insurance', {}).get('StandardClaimTime'), True),
            'ins_exp_claim_time': minutes(item['ship'].get('Insurance', {}).get('ExpeditedClaimTime'), True),
            'ins_exp_cost': integer(item['ship'].get('Insurance', {}).get('ExpeditedCost'), True),
        })
    return ships


def fix_vehicle_size(item):
    if item['ship'].get('IsVehicle', False):
        item['ship']['Size'] = 'Vehicle'


def find_guns(item):
    hardpoints = item['ports']['PilotHardpoints']
    mounts = []
    for hardpoint in hardpoints:
        loadout = hardpoint.get('Loadout', '')
        if 'Turret' in loadout:
            for port in hardpoint['InstalledItem']['Ports']:
                mounts.append(integer(port['Size']))
        else:
            mounts.append(integer(hardpoint['Size']))
    return mounts


def find_turrets(item):
    manned = item['ports']['MannedTurrets']
    remote = item['ports']['RemoteTurrets']
    mounts = []
    for turret in manned + remote:
        if (
            'InstalledItem' in turret
            and 'Turret' in turret['InstalledItem']['Type']
            and 'Ports' in turret['InstalledItem']
            and len(turret['InstalledItem']['Ports']) > 0
        ):
            mounts.append(integer(turret['InstalledItem']['Ports'][0]['Size']))
        else:
            mounts.append(integer(turret['Size']))
    return mounts


def find_missiles(item):
    racks = item['ports']['MissileRacks']
    mounts = []
    for rack in racks:
        if 'missilelauncher' in rack['PortName']:
            continue
        mounts.append(integer(rack['Size']))
    return mounts


if __name__ == '__main__':
    export()
