from pathlib import Path

import pytest
from click.testing import CliRunner

from .res import get_resource_filepath


@pytest.fixture(scope='module')
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope='module')
def path_stbl() -> Path:
    return get_resource_filepath('S4_220557DA_80000000_00000000598B0384.stbl')
