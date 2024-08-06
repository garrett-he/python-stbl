from click.testing import CliRunner

from stbl import __version__
from stbl.__cli__ import main


def test_cli_version(cli_runner: CliRunner):
    result = cli_runner.invoke(main, ['--version'])

    assert not result.exception
    assert result.output.strip() == __version__
