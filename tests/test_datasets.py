"""Tests for the datasets command group."""

import sys
from unittest.mock import MagicMock

import pandas as pd
from click.testing import CliRunner

from openml_cli.cli import main

# grab the shared mock injected by conftest.py
openml_mock = sys.modules["openml"]


def _make_datasets_df():
    """Create a sample datasets DataFrame matching the real API shape."""
    return pd.DataFrame({
        "did": [11, 12, 13],
        "name": ["Iris", "Adult", "MNIST"],
        "status": ["active", "active", "active"],
        "format": ["ARFF", "CSV", "CSV"],
        "version": ["1", "2", "1"],
    })


def test_datasets_list_basic():
    """Test basic dataset listing."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = _make_datasets_df()
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "list"])
    assert result.exit_code == 0
    assert "Found 3 dataset(s)" in result.output
    assert "Iris" in result.output
    assert "Adult" in result.output


def test_datasets_list_empty():
    """Test dataset listing when no datasets are found."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = pd.DataFrame()
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "list"])
    assert result.exit_code == 0
    assert "No datasets found" in result.output


def test_datasets_list_table_format():
    """Test dataset listing in table format."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = _make_datasets_df()
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "list", "--output", "table"])
    assert result.exit_code == 0
    assert "Found 3 dataset(s)" in result.output


def test_datasets_list_with_filters():
    """Test dataset listing with filter options."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = _make_datasets_df()
    runner = CliRunner()
    result = runner.invoke(
        main, ["datasets", "list", "--size", "5", "--status", "active"]
    )
    assert result.exit_code == 0
    openml_mock.datasets.list_datasets.assert_called_with(
        offset=None, size=5, tag=None, status="active", data_name=None,
    )


def test_datasets_info_valid():
    """Test getting info for a valid dataset ID."""
    openml_mock.datasets.get_dataset.reset_mock(side_effect=True)
    mock_ds = MagicMock()
    mock_ds.dataset_id = 11
    mock_ds.name = "Iris"
    mock_ds.version = 1
    mock_ds.format = "ARFF"
    mock_ds.creator = "R.A. Fisher"
    mock_ds.licence = "Public"
    mock_ds.collection_date = "1936"
    mock_ds.description = "The classic iris dataset."
    mock_ds.qualities = {"NumberOfInstances": 150, "NumberOfFeatures": 5}
    openml_mock.datasets.get_dataset.return_value = mock_ds

    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "info", "11"])
    assert result.exit_code == 0
    assert "Iris" in result.output
    assert "11" in result.output
    assert "ARFF" in result.output
    assert "NumberOfInstances" in result.output


def test_datasets_info_error():
    """Test getting info for a non-existent dataset."""
    openml_mock.datasets.get_dataset.reset_mock(side_effect=True)
    openml_mock.datasets.get_dataset.side_effect = Exception("Dataset not found")
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "info", "99999"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_datasets_search_match():
    """Test searching for datasets with matching results."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = _make_datasets_df()
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "search", "iris"])
    assert result.exit_code == 0
    assert "Found 1 dataset(s)" in result.output
    assert "Iris" in result.output


def test_datasets_search_no_match():
    """Test searching for datasets with no matching results."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = _make_datasets_df()
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "search", "NonExistent"])
    assert result.exit_code == 0
    assert "No datasets matching" in result.output


def test_datasets_search_empty_server():
    """Test search when server returns no datasets at all."""
    openml_mock.datasets.list_datasets.reset_mock(side_effect=True)
    openml_mock.datasets.list_datasets.return_value = pd.DataFrame()
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "search", "anything"])
    assert result.exit_code == 0
    assert "No datasets found on the server" in result.output


def test_datasets_help():
    """Test that datasets help message works."""
    runner = CliRunner()
    result = runner.invoke(main, ["datasets", "--help"])
    assert result.exit_code == 0
    assert "Browse and search" in result.output
