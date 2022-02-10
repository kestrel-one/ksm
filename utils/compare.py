def compare_ship_lists(old_ships, new_ships):
    old_index = compare_index(old_ships, 'id')
    new_index = compare_index(new_ships, 'id')
    diffs = []
    for old_ship in old_ships:
        new_ship = new_ships[new_index[old_ship['id']]]
        diffs.extend(compare_ships(old_ship, new_ship))
    for new_ship in new_ships:
        if new_ship['id'] not in old_index:
            diffs.append({
                'Ship Name': new_ship['name'],
                'Type': 'ship',
                'Old Value': None,
                'New Value': 'added',
                })
    return diffs


def compare_ships(old_ship, new_ship):
    fields = {}
    for field in old_ship:
        fields[field] = [old_ship[field], new_ship.get(field)]
    for field in new_ship:
        if field in fields:
            fields[field][1] = new_ship[field]
        else:
            fields[field] = [None, new_ship[field]]
    changes = {}
    for field in fields:
        values = fields[field]
        if values[0] != values[1]:
            changes[field] = values
    if len(changes) == 0:
        return []
    diffs = []
    for field in changes:
        diffs.append({
            'Ship Name': old_ship['name'],
            'Type': field,
            'Old Value': changes[field][0],
            'New Value': changes[field][1],
            })
    return diffs


def compare_index(items, field):
    index = {}
    for i, item in enumerate(items):
        index[item['id']] = i
    return index
