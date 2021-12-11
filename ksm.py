#! /usr/bin/env python

import click
import re
import sys

from utils.cli import render_json, render_table
from utils.sources import resolve_sources, source_choices

COL_GROUP_MAP = {
    'meta': ('source',),
    'basic': ('name', 'size'),
    'manufacturer': ('manufacturer_name', 'manufacturer_code'),
    'store': ('id', 'url', 'status', 'loaners'),
    'dimensions': ('mass', 'beam', 'height', 'length'),
    'flight': ('max_scm', 'max_speed'),
    'cargo': ('crew', 'max_crew', 'min_crew'),
    'weapons': ('num_weapons', 'num_guns', 'num_turrets', 'num_missiles', 'guns', 'turrets', 'missiles'),
    'prices': ('buy_auec', 'buy_usd', 'rent_auec'),
    'insurance': ('ins_std_claim_time', 'ins_exp_claim_time', 'ins_exp_cost'),
    'capabilities': ('has_quantum_drive', 'has_gravlev'),
}
COL_GROUP_MAP['all'] = \
    COL_GROUP_MAP['meta'] + \
    COL_GROUP_MAP['basic'] + \
    COL_GROUP_MAP['manufacturer'] + \
    COL_GROUP_MAP['store'] + \
    COL_GROUP_MAP['dimensions'] + \
    COL_GROUP_MAP['flight'] + \
    COL_GROUP_MAP['cargo'] + \
    COL_GROUP_MAP['weapons'] + \
    COL_GROUP_MAP['prices'] + \
    COL_GROUP_MAP['insurance'] + \
    COL_GROUP_MAP['capabilities']


@ click.group()
@ click.pass_context
def cli(ctx):
    ctx.max_content_width = 120


@ cli.command()
@ click.argument('sources', required=True, nargs=-1, type=source_choices)
def update(sources):
    modules = resolve_sources(sources)
    for name, module in modules:
        click.echo('Updating %s... ' % name)
        module.update()


@ cli.command()
@ click.argument('sources', required=True, nargs=-1, type=source_choices)
@ click.option('-n', '--names', multiple=True, type=str)
@ click.option('-c', '--cols', multiple=True, type=str)
@ click.option('-f', '--fmt', default='json', type=click.Choice(['json', 'table']))
@ click.option('-g', '--colgroups', multiple=True, type=click.Choice(COL_GROUP_MAP.keys()))
def dump(sources, names, cols, fmt, colgroups):
    ships = []
    for module_name, module in resolve_sources(sources):
        ships.extend([s for s in module.export() if match_name(s, names)])
    ships.sort(key=lambda k: (k['source'], k['name']))
    exports = [filter_cols(ship, cols) for ship in ships]
    for group in colgroups:
        cols += COL_GROUP_MAP[group]
    if len(cols) == 0:
        cols += COL_GROUP_MAP['all']
    if fmt == 'json':
        print(render_json(exports, cols))
    elif fmt == 'table':
        print(render_table(exports, cols))


def filter_cols(ship, cols):
    if len(cols) == 0:
        return ship
    item = {}
    for ship_col in ship:
        for col in cols:
            if match_str(col, ship_col):
                item[ship_col] = ship[ship_col]
    return item


def match_name(ship, allowed_names):
    if len(allowed_names) == 0:
        return True
    for name in allowed_names:
        find_name = name.lower()
        ship_name = ship['name'].lower()
        if match_str(find_name, ship_name):
            return True
    return False


def match_str(needle, haystack):
    if '*' in needle:
        regex = re.compile('^' + needle.replace('*', '.*') + '$')
        return regex.match(haystack) is not None
    return needle == haystack


if __name__ == '__main__':
    if len(sys.argv) == 1:
        cli.main(['--help'])
    else:
        cli()
