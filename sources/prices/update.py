import json
import pathlib
import requests
import time

from scrapy.selector import Selector
from utils.cli import progress

PAGE_URL = 'https://starcitizen.tools/List_of_pledge_vehicles'
DATA_PATH = pathlib.Path(__file__).parent / 'data.json'

def update():
    html = fetch()
    data = parse(html)
    save(data)


def fetch():
    html = ''
    with progress('Downloading', 1) as bar:
        # html = requests.get(PAGE_URL).content
        html = open('/tmp/vehicles.html').read()
        bar.update(1)
    return html


def parse(html):
    with progress('Parsing', 1) as bar:
        root = Selector(text=html)
        headers = []
        for th in root.css('table.plain-table.wikitable.sortable tr > th::text'):
            text = th.get().strip()
            text = text.replace(' ', '_')
            text = text.lower()
            headers.append(text)
        rows = []
        for tr in root.css('table.plain-table.wikitable.sortable tbody > tr'):
            cols = []
            for td in tr.css('td'):
                parts = [t.get().strip() for t in td.css('*::text')]
                cols.append(''.join(parts))
            if len(cols) == 0:
                continue
            row = {}
            for i, col in enumerate(cols):
                header = headers[i]
                row[header] = col
            rows.append(row)
        bar.update(1)
    for row in rows:
        if 'Liberator' not in row['name']:
            continue
        print(row)
    return rows


def save(data):
    with progress('Saving', 1) as bar:
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f)
        bar.update(1)


if __name__ == '__main__':
    update()
