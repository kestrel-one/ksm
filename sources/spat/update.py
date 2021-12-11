import pathlib
import requests

from utils.cli import progress

DATA_URL = 'https://docs.google.com/spreadsheets/d/11nI-wLlRjDpsshkY8VLZkHh2jd2mCmWJTIE2VzqZ7ss/gviz/tq?tqx=out:csv&sheet=AllShips'
DATA_PATH = pathlib.Path(__file__).parent / 'data.csv'
DATA_SIZE = 6 * 1024  # no content-length header, so we guess


def update():
    with progress('Fetching', 2) as bar:
        content = requests.get(DATA_URL).content
        bar.update(1)
        with open(DATA_PATH, 'wb') as f:
            f.write(content)
            bar.update(1)


if __name__ == '__main__':
    update()
