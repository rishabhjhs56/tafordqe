import pytest
import pandas as pd


import logging

import pytest

from reportportal_client import RPLogger


@pytest.fixture(scope="session")
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger


# -------------------------
# Fixture to read csv file
# -------------------------
@pytest.fixture(scope="session")
def read_csv_file():
    def _read(path_to_file):
        return pd.read_csv(path_to_file)
    return _read


# -------------------------
# Fixture to validate schema
# -------------------------
@pytest.fixture(scope="session")
def validate_schema():
    def _validate(actual_schema, expected_schema):
        return list(actual_schema) == list(expected_schema)
    return _validate


# -------------------------
# Hook to mark unmarked tests
# -------------------------
def pytest_collection_modifyitems(items):
    for item in items:
        if not item.own_markers:
            item.add_marker(pytest.mark.unmarked)


