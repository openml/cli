"""Tests for the OpenML CLI."""

from click.testing import CliRunner

from openml_cli import __version__
from openml_cli.cli import main


def test_version_command():
    """Test that the version command returns the correct version."""
    runner = CliRunner()
    result = runner.invoke(main, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_version_option():
    """Test that the --version option works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help_option():
    """Test that the --help option works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "OpenML command-line interface" in result.output
