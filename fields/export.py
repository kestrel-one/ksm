from collections import defaultdict

FIELD_GROUPS = {
    'meta': ('source',),
    'basic': ('id', 'name', 'size'),
    'manufacturer': ('manufacturer_name', 'manufacturer_code'),
    'store': ('url', 'status', 'loaners'),
    'dimensions': ('mass', 'beam', 'height', 'length'),
    'flight': ('scm_speed', 'max_speed'),
    'cargo': ('cargo', 'max_crew', 'min_crew'),
    'prices': ('buy_auec', 'buy_usd', 'rent_auec'),
    'insurance': ('ins_std_claim_time', 'ins_exp_claim_time', 'ins_exp_cost'),
    'capabilities': ('has_quantum_drive', 'has_gravlev'),
}

ALL_FIELDS = tuple(
    field
    for group in FIELD_GROUPS
    for field in FIELD_GROUPS[group]
)

FIELD_GROUPS['all'] = ALL_FIELDS

FIELD_SOURCES = {
    '__default__': ('spat', 'uex', 'scunpacked', 'rsi'),
    'name': ('rsi',),
    'manufacturer_name': ('rsi',),
    'manufacturer_code': ('rsi',),
    'id': ('rsi',),
    'url': ('rsi',),
    'status': ('rsi',),
    'min_crew': ('spat', 'scunpacked', 'rsi', 'uex'),
    'max_crew': ('spat', 'scunpacked', 'rsi', 'uex'),
    'buy_auec': ('scunpacked', 'uex'),
}

STATUS_LEVELS = {
    'Flight Ready': 3,
    'In Production': 2,
    'In Concept': 1,
}


def merge_fields(ships):
    index = create_index(ships)
    merged = []
    for ship_id, sources in index.items():
        ship = {}
        for field in ALL_FIELDS:
            if field == 'source':
                continue
            found = False
            for source in FIELD_SOURCES.get(field, FIELD_SOURCES['__default__']):
                if source in sources and field in sources[source]:
                    ship[field] = clean_value(sources[source][field])
                    found = True
                    break
            if not found:
                ship[field] = None
        merged.append(ship)
    return merged


def create_index(ships):
    index = defaultdict(dict)
    for ship in ships:
        index[ship['id']][ship['source']] = ship
    return index


def sort_value(ship, key):
    if key == 'status':
        return STATUS_LEVELS[ship['status']]
    return ship[key]


def clean_value(value):
    if type(value) == float and value.is_integer():
        return int(value)
    return value
