from collections import defaultdict


def inherit_field(index, ships, source, field):
    values_by_name = {}
    for ship in index.ships_by_source[source]:
        values_by_name[ship['name']] = ship[field]
    for i, ship in enumerate(ships):
        if ship['source'] == source:
            continue
        value = values_by_name.get(ship['name'])
        if value is None:
            raise ValueError('Index missing ship name: %s' % ship['name'])
        ships[i][field] = value


def copy_field_ship_to_ship(ships, field, from_ship, to_ship):
    best_value = None
    best_source = None
    for ship in ships:
        if ship['name'] != from_ship:
            continue
        value = ship.get(field)
        if value is not None:
            best_value = value
            best_source = ship['source']
    if best_value is None or best_source is None:
        return
    for ship in ships:
        if ship['name'] != to_ship:
            continue
        if ship['source'] != best_source:
            continue
        ship[field] = best_value


def clear_field_if_falsey(ships, field):
    for ship in ships:
        if field not in ship:
            continue
        if not ship[field]:
            ship[field] = None


def insert_field(ships, field, source, ship_name, value):
    for ship in ships:
        if ship['source'] != source:
            continue
        if ship['name'] != ship_name:
            continue
        ship[field] = value


def set_bool_field(ships, field):
    for i, ship in enumerate(ships):
        if field in ship:
            ships[i][field] = ship.get(field) or False


class Index:
    ships_by_source = defaultdict(list)

    def __init__(self, ships):
        for ship in ships:
            self.ships_by_source[ship['source']].append(ship)
