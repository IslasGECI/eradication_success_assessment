import pytest
from typer.testing import CliRunner
from eradication_success_assessment.get_required_effort import app


runner = CliRunner()


COMMANDS = ["write-methodology", "version", "get-required-effort"]


@pytest.mark.parametrize("command", COMMANDS)
def test_is_there_the_command(command):
    result = runner.invoke(app, [command])
    assert result.exit_code == 0
