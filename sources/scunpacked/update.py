import json
import os
import pathlib
import re
import requests
import tarfile

from utils.cli import progress

THIS_DIR = pathlib.Path(__file__).parent
DATA_URL = 'https://github.com/richardthombs/scunpacked/tarball/master'
SHIPS_DATA_PATH = THIS_DIR / 'ships.json'
SHOPS_DATA_PATH = THIS_DIR / 'shops.json'

ARCHIVE_SIZE = int(12.0 * 1024 ** 2)  # no content-length header, so we guess
ARCHIVE_PATH = THIS_DIR / 'data.tar.gz'

RE_SHIP_FILE = re.compile(r'.*/([a-zA-Z0-9_]+)(?:\-(ports|parts))?\.json$')


def update():
    fetch()
    unpack()
    cleanup()


def fetch():
    with progress('Downloading', ARCHIVE_SIZE) as bar:
        res = requests.get(DATA_URL, stream=True)
        with open(ARCHIVE_PATH, 'wb') as f:
            for data in res.iter_content(10 * 1024):
                bar.update(len(data))
                f.write(data)
            bar.update(ARCHIVE_SIZE)


def unpack():
    with tarfile.open(ARCHIVE_PATH, 'r:gz') as tar:
        ships, other = find_file_refs(tar)
        with progress('Unpacking ships', len(ships)) as bar:
            for name, files in ships.items():
                for key, filepath in files.items():
                    ships[name][key] = json.load(tar.extractfile(filepath))
                bar.update(1)
            with open(SHIPS_DATA_PATH, 'w') as f:
                json.dump(ships, f)
        with progress('Unpacking shops', 1) as bar:
            shops = json.load(tar.extractfile(other['shops']))
            with open(SHOPS_DATA_PATH, 'w') as f:
                json.dump(shops, f)
            bar.update(1)


def find_file_refs(tar):
    ships = {}
    other = {}
    for info in tar:
        if 'api/dist/json/v2/ships/' in info.name:
            match = RE_SHIP_FILE.match(info.name)
            if not match:
                continue
            name = match[1]
            category = match[2] or 'ship'
            if name not in ships:
                ships[name] = {}
            ships[name][category] = info.name
        if info.name.endswith('api/dist/json/shops.json'):
            other['shops'] = info.name
    return ships, other


def cleanup():
    os.remove(ARCHIVE_PATH)


if __name__ == '__main__':
    update()
