"""Tests for the flows command group."""

import sys
from unittest.mock import MagicMock

import pandas as pd
from click.testing import CliRunner

from openml_cli.cli import main

# grab the shared mock injected by conftest.py
openml_mock = sys.modules["openml"]


def _make_flows_df():
    """Create a sample flows DataFrame matching the real API shape."""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["RandomForest", "SVM", "RandomForestClassifier"],
        "full_name": ["RandomForest v1", "SVM v1", "RandomForestClassifier v1"],
        "version": ["1", "1", "2"],
        "external_version": ["1.0", "1.0", "2.0"],
        "uploader": ["100", "200", "100"],
    })


def test_flows_list_basic():
    """Test basic flow listing."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = _make_flows_df()
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "list"])
    assert result.exit_code == 0
    assert "Found 3 flow(s)" in result.output
    assert "RandomForest" in result.output
    assert "SVM" in result.output


def test_flows_list_empty():
    """Test flow listing when no flows are found."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = pd.DataFrame()
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "list"])
    assert result.exit_code == 0
    assert "No flows found" in result.output


def test_flows_list_table_format():
    """Test flow listing in table format."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = _make_flows_df()
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "list", "--output", "table"])
    assert result.exit_code == 0
    assert "Found 3 flow(s)" in result.output


def test_flows_list_with_filters():
    """Test flow listing with filter options."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = _make_flows_df()
    runner = CliRunner()
    result = runner.invoke(
        main, ["flows", "list", "--size", "10", "--tag", "sklearn"]
    )
    assert result.exit_code == 0
    openml_mock.flows.list_flows.assert_called_with(
        offset=None, size=10, tag="sklearn", uploader=None,
    )


def test_flows_info_valid():
    """Test getting info for a valid flow ID."""
    openml_mock.flows.get_flow.reset_mock(side_effect=True)
    mock_flow = MagicMock()
    mock_flow.flow_id = 123
    mock_flow.name = "sklearn.RandomForestClassifier"
    mock_flow.version = "3"
    mock_flow.description = "A random forest classifier."
    mock_flow.uploader = "42"
    mock_flow.upload_date = "2024-01-15"
    mock_flow.parameters = {"n_estimators": "100", "max_depth": "None"}
    mock_flow.tags = ["sklearn", "ensemble"]
    openml_mock.flows.get_flow.return_value = mock_flow

    runner = CliRunner()
    result = runner.invoke(main, ["flows", "info", "123"])
    assert result.exit_code == 0
    assert "123" in result.output
    assert "RandomForestClassifier" in result.output
    assert "n_estimators" in result.output
    assert "sklearn" in result.output


def test_flows_info_error():
    """Test getting info for a non-existent flow."""
    openml_mock.flows.get_flow.reset_mock(side_effect=True)
    openml_mock.flows.get_flow.side_effect = Exception("Flow not found")
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "info", "99999"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_flows_search_match():
    """Test searching for flows with matching results."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = _make_flows_df()
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "search", "random"])
    assert result.exit_code == 0
    assert "Found 2 flow(s)" in result.output
    assert "RandomForest" in result.output


def test_flows_search_no_match():
    """Test searching for flows with no matching results."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = _make_flows_df()
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "search", "XGBoost"])
    assert result.exit_code == 0
    assert "No flows matching" in result.output


def test_flows_search_empty_server():
    """Test search when server returns no flows at all."""
    openml_mock.flows.list_flows.reset_mock(side_effect=True)
    openml_mock.flows.list_flows.return_value = pd.DataFrame()
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "search", "anything"])
    assert result.exit_code == 0
    assert "No flows found on the server" in result.output


def test_flows_help():
    """Test that flows help message works."""
    runner = CliRunner()
    result = runner.invoke(main, ["flows", "--help"])
    assert result.exit_code == 0
    assert "Browse and search" in result.output
