FIELD_GROUPS = {
    'default': ('source', 'id', 'name', 'size', 'status', 'mass', 'beam', 'height', 'length'),
    'meta': ('source',),
    'basic': ('name', 'size'),
    'manufacturer': ('manufacturer_name', 'manufacturer_code'),
    'store': ('id', 'url', 'status', 'loaners'),
    'dimensions': ('mass', 'beam', 'height', 'length'),
    'flight': ('max_scm', 'max_speed'),
    'cargo': ('crew', 'max_crew', 'min_crew'),
    'prices': ('buy_auec', 'buy_usd', 'rent_auec'),
    'insurance': ('ins_std_claim_time', 'ins_exp_claim_time', 'ins_exp_cost'),
    'capabilities': ('has_quantum_drive', 'has_gravlev'),
}

ALL_FIELDS = tuple(field for group in FIELD_GROUPS for field in FIELD_GROUPS[group])
FIELD_GROUPS['all'] = ALL_FIELDS
