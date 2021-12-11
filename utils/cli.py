import click
import json
from prettytable import PrettyTable


def progress(label, length):
    return click.progressbar(
        length=length,
        width=10,
        label='% 12s' % label,
    )


def render_table(items, cols):
    table = PrettyTable()
    if len(cols) > 0:
        table.field_names = cols
        table.add_rows([[item.get(col, '') for col in cols] for item in items])
    else:
        cols = set()
        table.field_names = []
        table.add_rows(items)
    return table.get_string()


def render_json(items, cols):
    exports = [{col: item[col] for col in cols if col in item} for item in items]
    return json.dumps(exports, indent=2)
