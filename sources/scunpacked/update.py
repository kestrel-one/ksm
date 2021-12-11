import json
import os
import pathlib
import re
import requests
import tarfile

from utils.cli import progress

THIS_DIR = pathlib.Path(__file__).parent
# DATA_URL = 'https://github.com/richardthombs/scunpacked/tarball/master'
DATA_URL = 'https://github.com/kestrel-one/scunpacked/tarball/3_15_1'
DATA_PATH = THIS_DIR / 'data.json'

ARCHIVE_SIZE = int(12.0 * 1024 ** 2)  # no content-length header, so we guess
ARCHIVE_PATH = THIS_DIR / 'data.tar.gz'

RE_SHIP_FILE = re.compile(r'.*/([a-zA-Z0-9_]+)(?:\-(ports|parts))?\.json$')


def update():
    fetch()
    unpack()
    cleanup()


def fetch():
    with progress('Fetching', ARCHIVE_SIZE) as bar:
        res = requests.get(DATA_URL, stream=True)
        with open(ARCHIVE_PATH, 'wb') as f:
            for data in res.iter_content(10 * 1024):
                bar.update(len(data))
                f.write(data)
            bar.update(ARCHIVE_SIZE)


def unpack():
    with tarfile.open(ARCHIVE_PATH, 'r:gz') as tar:
        data = __build_data(tar)
        with progress('Unpacking', len(data)) as bar:
            for name, files in data.items():
                for key, filepath in files.items():
                    data[name][key] = json.load(tar.extractfile(filepath))
                bar.update(1)
            with open(DATA_PATH, 'w') as f:
                json.dump(data, f)


def __build_data(tar):
    data = {}
    for info in tar:
        if 'api/dist/json/v2/ships/' not in info.name:
            continue
        match = RE_SHIP_FILE.match(info.name)
        if not match:
            continue
        name = match[1]
        sect = match[2] or 'ship'
        if name not in data:
            data[name] = {}
        data[name][sect] = info.name
    return data


def cleanup():
    os.remove(ARCHIVE_PATH)


if __name__ == '__main__':
    update()
