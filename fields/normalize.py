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


def set_bool_field(ships, field):
    for i, ship in enumerate(ships):
        if field in ship:
            ships[i][field] = ship.get(field) or False


class Index:
    ships_by_source = defaultdict(list)

    def __init__(self, ships):
        for ship in ships:
            self.ships_by_source[ship['source']].append(ship)
