import click

from stbl.__about__ import __version__
from stbl.commands import command_group


def print_version(ctx: click.Context, _, value: str):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group(commands=command_group)
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def main():
    """A package including command-line utilities to parse *.stbl files for modding game: The Sims."""


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
