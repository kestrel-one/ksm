from collections import defaultdict

FIELD_GROUPS = {
    'meta': ('source',),
    'basic': ('id', 'name', 'size'),
    'manufacturer': ('manufacturer_name', 'manufacturer_code'),
    'store': ('url', 'status', 'loaners'),
    'dimensions': ('mass', 'beam', 'height', 'length'),
    'flight': ('scm_speed', 'max_speed'),
    'cargo': ('crew', 'max_crew', 'min_crew'),
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
}


def merge_fields(ships):
    index = defaultdict(dict)
    for ship in ships:
        index[ship['id']][ship['source']] = ship
    merged = []
    for ship_id, sources in index.items():
        ship = {}
        for field in ALL_FIELDS:
            if field == 'source':
                continue
            found = False
            for source in FIELD_SOURCES.get(field, FIELD_SOURCES['__default__']):
                if source in sources and field in sources[source]:
                    ship[field] = sources[source][field]
                    found = True
                    break
            if not found:
                ship[field] = None
        merged.append(ship)
    return merged
