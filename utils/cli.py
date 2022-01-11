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
        w.writerow(render_text_row(item, cols))
    return out.getvalue()


def render_table(items, cols):
    table = PrettyTable()
    table.field_names = cols
    for item in items:
        table.add_row(render_text_row(item, cols))
    return table.get_string()


def render_text_row(item, cols):
    row = []
    for col in cols:
        val = item.get(col, '')
        if val is None:
            val = '-'
        row.append(val)
    return row


def render_json(items, cols):
    exports = [{col: item[col] for col in cols if col in item} for item in items]
    return json.dumps(exports, indent=2)
