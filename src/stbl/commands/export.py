import json

import click

from stbl.stbl import STBLFile


@click.command('export')
@click.argument('stbl_file', type=click.Path(exists=True, dir_okay=False))
def export_command(stbl_file):
    """Export .stbl file in JSON format."""

    stbl = STBLFile()
    stbl.read(stbl_file)

    if not stbl.validate():
        raise RuntimeError(f'Invalid .stbl file format "{stbl_file}".')

    data = list(map(lambda entry: {'instance': '0x' + ('%08x' % entry.instance_id).upper(), 'text': entry.text}, stbl.entries))

    print(json.dumps(data, ensure_ascii=False, indent=4))
