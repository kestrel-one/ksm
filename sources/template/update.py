import json
import os
import requests
import pathlib
import tarfile

from utils.cli import progress


# XXX
THIS_DIR = pathlib.Path(__file__).parent
DATA_URL = ''
DATA_PATH = THIS_DIR / 'data.json'

# XXX
ARCHIVE_SIZE = 10 * 1024 ** 2  # no content-length header, so we guess
ARCHIVE_PATH = THIS_DIR / 'data.tar.gz'


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
    with progress('Unpacking', 2) as bar:
        data = None
        with tarfile.open(ARCHIVE_PATH, 'r:gz') as tar:
            data = json.loads(__build_data(tar))
            bar.update(1)
        with open(DATA_PATH, 'w') as f:
            json.dump([data[key] for key in data], f)
            bar.update(1)


def cleanup():
    os.remove(ARCHIVE_PATH)


def __build_data(tar):
    for info in tar:
        if info.name == info.name:  # XXX
            contents = tar.extractfile(info.name).read().decode('utf-8')
            contents = contents.strip()  # XXX
            return contents
    return None


if __name__ == '__main__':
    update()
