import re

from fields.types import integer

RE_MANUFACTURER_PREFIX = re.compile(
    r'^(Aegis|Anvil|Aopoa|Argo|Banu|C\.O\.|Crusader|Drake|Esperia|Greycat|'
    'Kruger|MISC|Origin|RSI|Tumbril|Vanduul) ')
RE_SHIP_CLASS_SEPARATOR = re.compile(r'^(Aurora|Cyclone)-([A-Z]{1,2})$')
RE_G12_DASH_NAME = re.compile(r'^G12-([A-Z]{1,2})$')
RE_CRUSADER_STAR = re.compile(r' (Starlifter|Star Runner)$')
RE_STARFIGHTER = re.compile(r'^Ares Star Fighter')
RE_URL_PREFIX = re.compile(r'^[a-z0-9]*:\/\/', re.IGNORECASE)

SHIP_RENAME_MAP = {
    'Idris': 'Idris-M',
    'Retaliator': 'Retaliator Bomber',
    'F7C-M Hornet Heartseeker': 'F7C-M Super Hornet Heartseeker',
    'Dragonfly': 'Dragonfly Black',
    '600i': '600i Explorer',
    '85X Limited': '85X',
    'M50 Interceptor': 'M50',
    'P72 Archimedes': 'P-72 Archimedes',
    'P72 Archimedes Emerald': 'P-72 Archimedes Emerald',
    'Khartu-Al': 'Khartu-al',
    'Pirate Gladius': 'Gladius Pirate',
    'San tok.Yāi': "San'tok.yāi",
    'Mole': 'MOLE',
    'MPUV-1C': 'MPUV Cargo',
    'MPUV-1P': 'MPUV Personnel',
    'Genesis Starliner': 'Genesis',
    'Nova Tank': 'Nova',
    'Enveador': 'Endeavor',
}

SHIP_SKIP_MAP = (
    'Ballista Dunestalker',
    'Ballista Snowblind',
    'Constellation Phoenix Emerald',
    'Dragonfly Yellowjacket',
    'F8 Lightning',
    'Mustang Alpha Vindicator',
    'P-72 Archimedes Emerald',
    'PTV',
    'Ursa Rover Fortuna',
)

SHIP_SIZE_MAP = {
    '1': 'Snub',
    '2': 'Small',
    '3': 'Medium',
    '4': 'Large',
    '5': 'Large',
    '6': 'Capital',
}

SHIP_SIZES = ('Snub', 'Small', 'Medium', 'Large', 'Capital', 'Vehicle')


def is_skippable_ship_name(name):
    return name.endswith(' Edition') or name in SHIP_SKIP_MAP


def ship_name(name):
    name = name.strip()
    name = RE_MANUFACTURER_PREFIX.sub('', name)
    name = RE_SHIP_CLASS_SEPARATOR.sub('\\1 \\2', name)
    name = RE_G12_DASH_NAME.sub(lambda m: 'G12' + m.group(1).lower(), name)
    name = RE_CRUSADER_STAR.sub('', name)
    name = RE_STARFIGHTER.sub('Ares', name)
    name = SHIP_RENAME_MAP.get(name, name)
    return None if is_skippable_ship_name(name) else name


def ship_size(size, name):
    if size is None:
        if name == 'G12':
            size = 'Vehicle'
        elif name == 'Railen':
            size = 'Small'
        elif name == 'Nomad':
            size = 'Medium'
    if type(size) == int:
        size = str(size)
    if size in SHIP_SIZE_MAP:
        size = SHIP_SIZE_MAP[size]
    if type(size) != str:
        raise ValueError('Unknown ship size "%s" for ship "%s"' % (size, name))
    size = size.strip().lower().capitalize()
    if size not in SHIP_SIZES:
        raise ValueError('Unknown ship size "%s"' % size)
    return size.lower()


def ship_status(status):
    status = status.strip()
    if status == 'flight-ready':
        return 'Flight Ready'
    elif status == 'in-production':
        return 'In Production'
    elif status == 'in-concept':
        return 'In Concept'
    raise ValueError('Unknown status: {}' % status)


def ship_url(path_or_url):
    if RE_URL_PREFIX.match(path_or_url):
        return path_or_url
    if len(path_or_url) > 0 and path_or_url[0] != '/':
        path_or_url = '/' + path_or_url
    return 'https://robertsspaceindustries.com' + path_or_url


def ship_manu_code(code):
    return code.strip()


def ship_manu_name(name):
    return name.strip()


def ship_crew_range(s):
    parts = s.split('-')
    min_crew = integer(parts[0])
    max_crew = integer(parts[1] if len(parts) > 1 else min_crew)
    return (min_crew, max_crew)
