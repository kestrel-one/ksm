import pathlib
import requests

from utils.cli import progress

DATA_URL = 'https://robertsspaceindustries.com/ship-matrix/index'
DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def update():
    content = None
    with progress('Downloading', 1) as bar:
        content = requests.get(DATA_URL).content
        bar.update(1)
    with open(DATA_PATH, 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    update()
