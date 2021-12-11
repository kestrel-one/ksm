import math


def integer(value, optional=False):
    if optional and value is None:
        return value
    t = type(value)
    if t == float and value.is_integer():
        return int(value)
    if t == int:
        return value
    elif t == str:
        return int(value)
    raise TypeError('Unknown number type: %s' % t)


def decimal(value, optional=False):
    if optional and value is None:
        return None
    t = type(value)
    if t == float:
        return value
    elif t == str or t == int:
        return float(value)
    raise TypeError('Unknown decimal type: %s' % t)


def minutes(value, optional=False):
    if optional and value is None:
        return None
    base = math.floor(value)
    hrs = math.floor(base / 60.0)
    min = base % 60.0
    sec = round(60 * (value - base))
    return '%02d:%02d:%02d' % (hrs, min, sec)
