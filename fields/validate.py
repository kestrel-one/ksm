from fields.export import create_index, ALL_FIELDS, FIELD_GROUPS


def validate_fields(ships, merged_ships):
    index = create_index(ships)
    problems = []

    # find missing required fields
    required_fields = ('id', 'name', 'source')
    for ship in ships:
        for field in required_fields:
            if field not in ship:
                problems.append('Missing ID in record: ' + repr(ship))

    # every field must have at least one value
    # every field must be the same-ish type
    for field in ALL_FIELDS:
        values = []
        for ship_id, sources in index.items():
            for source, ship in sources.items():
                values.append(ship.get(field))
        if all([not value for value in values]):
            problems.append('Field "%s" is always falsey' % field)
        typed_no_none = set([type(v) for v in values if v is not None])
        if len(typed_no_none) != 1:
            problems.append('Field "%s" is not all the same type: %s' % (field, values))

    # there should be no vehicles with a QD
    for ship in merged_ships:
        if ship['size'] == 'Vehicle' and ship['has_quantum_drive']:
            problems.append('Ship "%s" is a vehicle with a quantum drive' % ship['name'])

    # all flight ready ships should have insurance info
    for ship in merged_ships:
        for field in FIELD_GROUPS['insurance']:
            if ship['status'] != 'Flight Ready':
                continue
            if not ship.get(field):
                problems.append('Flight ready ship "%s" missing insurance info: %s' % (ship['name'], field))

    return problems
