import click
import csv
import io
import json
from prettytable import PrettyTable


def progress(label, length):
    return click.progressbar(
        length=length,
        width=10,
        label='% 16s' % label,
    )


def render_csv(items, cols):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(cols)
    for item in items:
        w.writerow([item.get(col, '') for col in cols])
    return out.getvalue()


def render_table(items, cols):
    table = PrettyTable()
    table.field_names = cols
    table.add_rows([[item.get(col, '') for col in cols] for item in items])
    return table.get_string()


def render_json(items, cols):
    exports = [{col: item[col] for col in cols if col in item} for item in items]
    return json.dumps(exports, indent=2)
