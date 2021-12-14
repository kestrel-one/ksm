import click
import os
import pathlib
import requests

from utils.cli import progress

DATA_URL = 'https://api.uexcorp.space/ships'
DATA_PATH = pathlib.Path(__file__).parent / 'data.json'


def update():
    api_key = os.environ.get('UEX_API_KEY')
    if not api_key:
        click.echo('  Skipping. UEX_API_KEY is not set. See: https://uexcorp.space/api.html')
        return
    with progress('Downloading', 2) as bar:
        content = requests.get(DATA_URL, headers={'api_key': api_key}).content
        bar.update(1)
        with open(DATA_PATH, 'wb') as f:
            f.write(content)
            bar.update(1)


if __name__ == '__main__':
    update()
