"""Shared test fixtures for the CLI test suite."""

import sys
from unittest.mock import MagicMock

# create a single shared mock for the openml package so that all
# lazy imports inside CLI command modules resolve to this mock.
# this must run before any command module is imported.
openml_mock = MagicMock()
sys.modules["openml"] = openml_mock
sys.modules["openml.flows"] = openml_mock.flows
sys.modules["openml.datasets"] = openml_mock.datasets
sys.modules["openml.tasks"] = openml_mock.tasks
sys.modules["openml.runs"] = openml_mock.runs
sys.modules["openml.config"] = openml_mock.config
