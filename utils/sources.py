import click
import sources

all_sources = [(n, m) for n, m in sources.__dict__.items() if not n.startswith('__')]
source_names = [n for n, _ in all_sources]
source_table = dict(all_sources)
source_choices = click.Choice(source_names + ['all'])


def resolve_sources(names):
    if 'all' in names:
        return all_sources
    return [(n, m) for n, m in all_sources if n in names]
