def compare_ship_lists(ships1, ships2):
    index2 = compare_index(ships2, 'id')
    diffs = []
    for ship1 in ships1:
        ship2 = ships2[index2[ship1['id']]]
        diffs.extend(compare_ships(ship1, ship2))
    return diffs


def compare_ships(ship1, ship2):
    fields = {}
    for field in ship1:
        fields[field] = [ship1[field], ship2.get(field)]
    for field in ship2:
        if field in fields:
            fields[field][1] = ship2[field]
        else:
            fields[field] = [None, ship2[field]]
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
            'Ship Name': ship1['name'],
            'Field Name': field,
            'Old Value': changes[field][0],
            'New Value': changes[field][1],
            })
    return diffs


def compare_index(items, field):
    index = {}
    for i, item in enumerate(items):
        index[item['id']] = i
    return index
