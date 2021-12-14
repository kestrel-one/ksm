#! /usr/bin/env python

import click
import re
import sys

from fields.export import merge_fields, sort_value, ALL_FIELDS, FIELD_GROUPS
from fields.normalize import (
    Index,
    clear_field_if_falsey,
    copy_field_ship_to_ship,
    inherit_field,
    insert_field,
    set_bool_field,
)
from fields.validate import validate_fields
from utils.cli import render_csv, render_json, render_table
from utils.sources import all_sources, resolve_sources, source_choices

DEFAULT_SORT = ('source.asc', 'name.asc')
EXPORT_SORT = ('status.desc', 'manufacturer_code.asc', 'name.asc')

RENDERERS = {
    'csv': render_csv,
    'json': render_json,
    'table': render_table,
}


@ click.group()
@ click.pass_context
@click.version_option('2.1.3')
def cli(ctx):
    ctx.max_content_width = 120
    ctx.help_option_names = ['-h', '--help']


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
@ click.option('-c', '--cols', multiple=True, type=click.Choice(ALL_FIELDS))
@ click.option('-f', '--fmt', default='json', type=click.Choice(RENDERERS.keys()))
@ click.option('-g', '--colgroups', multiple=True, type=click.Choice(FIELD_GROUPS.keys()))
@ click.option('-s', '--sort', default=DEFAULT_SORT, multiple=True, type=str, help='[column].[asc|desc] (eg: source.desc)')
def dump(sources, names, cols, fmt, colgroups, sort):
    resolved_sources = resolve_sources(sources)
    ships = [
        ship for ship in export_all()
        if match_name(ship, names)
        and match_source(ship, resolved_sources)]
    cols = resolve_cols(cols, colgroups, 'all')
    sort_ships(ships, sort)
    ships = [filter_cols(ship, cols) for ship in ships]
    print(RENDERERS[fmt](ships, cols))


@cli.command()
@ click.option('-n', '--names', multiple=True, type=str)
@ click.option('-c', '--cols', multiple=True, type=click.Choice(ALL_FIELDS))
@ click.option('-f', '--fmt', default='json', type=click.Choice(RENDERERS.keys()))
@ click.option('-g', '--colgroups', multiple=True, type=click.Choice(FIELD_GROUPS.keys()))
@ click.option('-s', '--sort', default=EXPORT_SORT, multiple=True, type=str, help='[column].[asc|desc] (eg: source.desc)')
def export(names, cols, fmt, colgroups, sort):
    ships = [ship for ship in export_all() if match_name(ship, names)]
    ships = merge_fields(ships)
    cols = resolve_cols(cols, colgroups, 'all', no_source=True)
    sort_ships(ships, sort)
    exports = [filter_cols(ship, cols) for ship in ships]
    print(RENDERERS[fmt](exports, cols))


@cli.command()
def validate():
    ships = export_all()
    merged_ships = merge_fields(ships)
    for problem in validate_fields(ships, merged_ships):
        print(problem)


def resolve_cols(cols, groups, default_group, no_source=False):
    cols = tuple(col for group in groups for col in FIELD_GROUPS[group]) + cols
    if len(cols) == 0:
        cols += FIELD_GROUPS[default_group]
    if no_source:
        cols = [col for col in cols if col != 'source']
    return cols


def export_all():
    ships = []
    for module_name, module in all_sources:
        ships.extend([s for s in module.export()])
    index = Index(ships)
    inherit_field(index, ships, 'rsi', 'id')

    copy_field_ship_to_ship(ships, 'ins_std_claim_time', '600i Touring', '600i Explorer')
    copy_field_ship_to_ship(ships, 'ins_exp_claim_time', '600i Touring', '600i Explorer')
    copy_field_ship_to_ship(ships, 'ins_exp_cost', '600i Touring', '600i Explorer')

    insert_field(ships, 'ins_std_claim_time', 'scunpacked', 'MOLE', '00:16:12')
    insert_field(ships, 'ins_exp_claim_time', 'scunpacked', 'MOLE', '00:02:42')
    insert_field(ships, 'ins_exp_cost', 'scunpacked', 'MOLE', 4050)

    set_bool_field(ships, 'has_gravlev')
    set_bool_field(ships, 'has_quantum_drive')

    clear_field_if_falsey(ships, 'buy_usd')
    clear_field_if_falsey(ships, 'buy_auec')
    return ships


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
        if match_str(name.lower(), ship['name'].lower()):
            return True
    return False


def match_source(ship, allowed_sources):
    if len(allowed_sources) == 0:
        return True
    for name, _ in allowed_sources:
        if ship['source'] == name:
            return True
    return False


def match_str(needle, haystack):
    if '*' in needle:
        regex = re.compile('^' + needle.replace('*', '.*') + '$')
        return regex.match(haystack) is not None
    return needle == haystack


def sort_ships(ships, sort_keys):
    ships.sort(key=lambda k: create_sort_key(k, sort_keys))


def create_sort_key(ship, sort_keys):
    resolved_keys = []
    for key in sort_keys:
        key_name, order = (key if '.' in key else key + '.asc').split('.')
        resolved_keys.append(str_sort_key(sort_value(ship, key_name), order))
    return resolved_keys


def str_sort_key(value, order):
    if order == 'asc':
        return value
    if order == 'desc':
        return reverse_sort_key(value)
    raise ValueError('Unknown sort order: %s' % order)


def reverse_sort_key(value):
    t = type(value)
    if t == str:
        return [255 - ord(c) for c in list(value)]
    elif t == int or t == float:
        return -value
    return ValueError('Cannot reverse key of type: %s' % t)


if __name__ == '__main__':
    cli(['--help'] if len(sys.argv) == 1 else None)
