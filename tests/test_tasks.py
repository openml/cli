"""Tests for the tasks command group."""

import sys
from unittest.mock import MagicMock

import pandas as pd
from click.testing import CliRunner

from openml_cli.cli import main

# grab the shared mock injected by conftest.py
openml_mock = sys.modules["openml"]


def _make_tasks_df():
    """Create a sample tasks DataFrame matching the real API shape."""
    return pd.DataFrame({
        "tid": [1, 2, 3],
        "name": ["iris-classify", "adult-classify", "mnist-classify"],
        "task_type": ["Supervised Classification"] * 3,
        "did": [11, 12, 13],
        "status": ["active"] * 3,
    })


def test_tasks_list_basic():
    """Test basic task listing."""
    openml_mock.tasks.list_tasks.reset_mock(side_effect=True)
    openml_mock.tasks.list_tasks.return_value = _make_tasks_df()
    runner = CliRunner()
    result = runner.invoke(main, ["tasks", "list"])
    assert result.exit_code == 0
    assert "Found 3 task(s)" in result.output
    assert "iris-classify" in result.output


def test_tasks_list_empty():
    """Test task listing when no tasks are found."""
    openml_mock.tasks.list_tasks.reset_mock(side_effect=True)
    openml_mock.tasks.list_tasks.return_value = pd.DataFrame()
    runner = CliRunner()
    result = runner.invoke(main, ["tasks", "list"])
    assert result.exit_code == 0
    assert "No tasks found" in result.output


def test_tasks_list_table_format():
    """Test task listing in table format."""
    openml_mock.tasks.list_tasks.reset_mock(side_effect=True)
    openml_mock.tasks.list_tasks.return_value = _make_tasks_df()
    runner = CliRunner()
    result = runner.invoke(main, ["tasks", "list", "--output", "table"])
    assert result.exit_code == 0
    assert "Found 3 task(s)" in result.output


def test_tasks_list_with_filters():
    """Test task listing with filter options."""
    openml_mock.tasks.list_tasks.reset_mock(side_effect=True)
    openml_mock.tasks.list_tasks.return_value = _make_tasks_df()
    runner = CliRunner()
    result = runner.invoke(
        main, ["tasks", "list", "--size", "5", "--status", "active"]
    )
    assert result.exit_code == 0


def test_tasks_info_valid():
    """Test getting info for a valid task ID."""
    openml_mock.tasks.get_task.reset_mock(side_effect=True)
    mock_task = MagicMock()
    mock_task.task_id = 1
    mock_task.task_type = "Supervised Classification"
    mock_task.dataset_id = 11
    mock_task.target_name = "class"
    mock_task.estimation_procedure_type = "10-fold Crossvalidation"
    mock_task.evaluation_measure = "predictive_accuracy"
    openml_mock.tasks.get_task.return_value = mock_task

    runner = CliRunner()
    result = runner.invoke(main, ["tasks", "info", "1"])
    assert result.exit_code == 0
    assert "Supervised Classification" in result.output
    assert "class" in result.output
    assert "10-fold" in result.output


def test_tasks_info_error():
    """Test getting info for a non-existent task."""
    openml_mock.tasks.get_task.reset_mock(side_effect=True)
    openml_mock.tasks.get_task.side_effect = Exception("Task not found")
    runner = CliRunner()
    result = runner.invoke(main, ["tasks", "info", "99999"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_tasks_help():
    """Test that tasks help message works."""
    runner = CliRunner()
    result = runner.invoke(main, ["tasks", "--help"])
    assert result.exit_code == 0
    assert "Browse OpenML tasks" in result.output
