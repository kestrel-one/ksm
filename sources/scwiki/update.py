import json
import pathlib
import requests
import time

from scrapy.selector import Selector
from utils.cli import progress

VEHICLES_PAGE_URL = 'https://starcitizen.tools/List_of_pledge_vehicles'
RENTALS_PAGE_URL = 'https://starcitizen.tools/Ship_renting'

DATA_PATH = pathlib.Path(__file__).parent / 'data.json'

def update():
    pages = fetch()
    data = parse(pages)
    save(data)


def fetch():
    vehicles = ''
    rentals = ''
    with progress('Downloading', 2) as bar:
        vehicles = requests.get(VEHICLES_PAGE_URL).content
        bar.update(1)
        rentals = requests.get(RENTALS_PAGE_URL).content
        bar.update(1)
    return {'vehicles': vehicles, 'rentals': rentals}


def parse(pages):
    data = {}
    with progress('Parsing', 1) as bar:
        data['vehicles'] = parse_vehicles(pages['vehicles'])
        bar.update(1)
        data['rentals'] = parse_rentals(pages['rentals'])
        bar.update(1)
    return data


def parse_vehicles(html):
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
    return rows


def parse_rentals(html):
    root = Selector(text=html)
    prices = []
    for table in root.css('table.wikitable'):
        headings = table.css('tr:first-child > th')
        heading3 = headings[2].css('::text').get().strip()
        if 'Period' not in heading3:
            continue
        location = table.xpath('preceding-sibling::h4[1]').css('*::text').get()
        rows = table.css('tr')
        last_manufacturer = ''
        for i, tr in enumerate(rows):
            if i < 2:
                continue
            cols = []
            for td in tr.css('td'):
                parts = [t.get().strip() for t in td.css('*::text')]
                cols.append(''.join(parts))
            start_index = 0
            manufacturer = ''
            if len(cols) == 5:
                start_index = 0
            else:
                last_manufacturer = cols[0]
                start_index = 1
            prices.append({
                'location': location,
                'manufacturer': last_manufacturer,
                'ship': cols[start_index],
                '1day': cols[start_index + 1],
                '3day': cols[start_index + 2],
                '7day': cols[start_index + 3],
                '30day': cols[start_index + 4],
                })
    return prices


def save(data):
    with progress('Saving', 1) as bar:
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f)
        bar.update(1)


if __name__ == '__main__':
    update()
