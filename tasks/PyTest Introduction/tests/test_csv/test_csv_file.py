import pytest
import re
import os

CURRENT_DIR = os.path.dirname(__file__)

FILE_PATH = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..", "src", "data", "data.csv")
)
# -----------------------------------
# Validate file not empty
# -----------------------------------
def test_file_not_empty(read_csv_file):
    df = read_csv_file(FILE_PATH)
    assert not df.empty, "CSV file is empty."


# -----------------------------------
# Validate schema
# -----------------------------------
@pytest.mark.validate_csv
def test_validate_schema(read_csv_file, validate_schema):
    df = read_csv_file(FILE_PATH)

    expected_schema = ["id", "name", "age", "email", "is_active"]
    actual_schema = df.columns.tolist()

    assert validate_schema(actual_schema, expected_schema), \
        f"Schema mismatch. Expected {expected_schema}, got {actual_schema}"


# -----------------------------------
# Validate age (skip)
# -----------------------------------
@pytest.mark.validate_csv
@pytest.mark.skip(reason="Skipping age validation temporarily")
def test_validate_age(read_csv_file):
    df = read_csv_file(FILE_PATH)

    assert df["age"].between(0, 100).all(), \
        "Age column contains invalid values."


# -----------------------------------
# Validate email format
# -----------------------------------
@pytest.mark.validate_csv
def test_validate_email(read_csv_file):
    df = read_csv_file(FILE_PATH)

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    invalid_emails = df[
        ~df["email"].astype(str).str.match(pattern)
    ]

    assert invalid_emails.empty, \
        f"Invalid emails found: {invalid_emails['email'].tolist()}"


# -----------------------------------
# Duplicate rows (xfail)
# -----------------------------------
@pytest.mark.validate_csv
@pytest.mark.xfail(reason="Known issue - duplicate rows present")
def test_no_duplicates(read_csv_file):
    df = read_csv_file(FILE_PATH)

    assert not df.duplicated().any(), \
        "Duplicate rows found."


# -----------------------------------
# Parametrize test
# -----------------------------------
@pytest.mark.parametrize(
    "user_id, status",
    [
        (1, False),
        (2, True)
    ]
)
def test_is_active_parametrize(read_csv_file, user_id, status):
    df = read_csv_file(FILE_PATH)

    actual = df[df["id"] == user_id]["is_active"].iloc[0]

    assert actual == status, \
        f"id={user_id} expected {status}, got {actual}"


# -----------------------------------
# Same for id=2 without parametrize
# -----------------------------------
def test_is_active_for_id_2(read_csv_file):
    df = read_csv_file(FILE_PATH)

    actual = df[df["id"] == 2]["is_active"].iloc[0]

    assert actual == True, \
        f"id=2 expected True, got {actual}"
    

# In this case only INFO messages will be sent to the ReportPortal.
def test_one(rp_logger):
    rp_logger.info("Case1. Step1")

    x = "this"

    rp_logger.info("x is: %s", x)

    assert 'h' in x

    rp_logger.info("Execution completed")