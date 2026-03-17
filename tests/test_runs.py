"""Tests for the runs command group."""

import sys
from unittest.mock import MagicMock

import pandas as pd
from click.testing import CliRunner

from openml_cli.cli import main

# grab the shared mock injected by conftest.py
openml_mock = sys.modules["openml"]


def _make_runs_df():
    """Create a sample runs DataFrame matching the real API shape."""
    return pd.DataFrame({
        "run_id": [100, 200, 300],
        "task_id": [1, 2, 3],
        "flow_id": [10, 20, 30],
        "setup_id": [5, 6, 7],
        "uploader": [42, 42, 99],
    })


def test_runs_list_basic():
    """Test basic run listing."""
    openml_mock.runs.list_runs.reset_mock(side_effect=True)
    openml_mock.runs.list_runs.return_value = _make_runs_df()
    runner = CliRunner()
    result = runner.invoke(main, ["runs", "list"])
    assert result.exit_code == 0
    assert "Found 3 run(s)" in result.output
    assert "100" in result.output


def test_runs_list_empty():
    """Test run listing when no runs are found."""
    openml_mock.runs.list_runs.reset_mock(side_effect=True)
    openml_mock.runs.list_runs.return_value = pd.DataFrame()
    runner = CliRunner()
    result = runner.invoke(main, ["runs", "list"])
    assert result.exit_code == 0
    assert "No runs found" in result.output


def test_runs_list_table_format():
    """Test run listing in table format."""
    openml_mock.runs.list_runs.reset_mock(side_effect=True)
    openml_mock.runs.list_runs.return_value = _make_runs_df()
    runner = CliRunner()
    result = runner.invoke(main, ["runs", "list", "--output", "table"])
    assert result.exit_code == 0
    assert "Found 3 run(s)" in result.output


def test_runs_list_with_filters():
    """Test run listing with comma-separated ID filters."""
    openml_mock.runs.list_runs.reset_mock(side_effect=True)
    openml_mock.runs.list_runs.return_value = _make_runs_df()
    runner = CliRunner()
    result = runner.invoke(
        main, ["runs", "list", "--task", "1,2", "--tag", "study_1"]
    )
    assert result.exit_code == 0
    openml_mock.runs.list_runs.assert_called_with(
        offset=None, size=None,
        id=None, task=[1, 2], flow=None, uploader=None,
        tag="study_1", study=None,
    )


def test_runs_info_valid():
    """Test getting info for a valid run ID."""
    openml_mock.runs.get_run.reset_mock(side_effect=True)
    mock_run = MagicMock()
    mock_run.run_id = 100
    mock_run.task_id = 1
    mock_run.flow_id = 10
    mock_run.flow_name = "sklearn.RandomForest"
    mock_run.setup_id = 5
    mock_run.uploader = 42
    mock_run.evaluations = {"predictive_accuracy": 0.95, "f_measure": 0.93}
    mock_run.tags = ["benchmark"]
    openml_mock.runs.get_run.return_value = mock_run

    runner = CliRunner()
    result = runner.invoke(main, ["runs", "info", "100"])
    assert result.exit_code == 0
    assert "100" in result.output
    assert "RandomForest" in result.output
    assert "predictive_accuracy" in result.output
    assert "0.95" in result.output
    assert "benchmark" in result.output


def test_runs_info_error():
    """Test getting info for a non-existent run."""
    openml_mock.runs.get_run.reset_mock(side_effect=True)
    openml_mock.runs.get_run.side_effect = Exception("Run not found")
    runner = CliRunner()
    result = runner.invoke(main, ["runs", "info", "99999"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_runs_help():
    """Test that runs help message works."""
    runner = CliRunner()
    result = runner.invoke(main, ["runs", "--help"])
    assert result.exit_code == 0
    assert "Browse OpenML runs" in result.output
