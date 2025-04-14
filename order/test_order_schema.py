#!/usr/bin/env python
# coding: utf-8

import jsonschema
import yaml
import json
import pytest  # Import pytest
from jsonschema.exceptions import ValidationError

# Define test data folder at module level
dataFolder = "testData"

# Load schema once at module level
try:
    with open("./order.yaml", "r") as f:
        schema = yaml.safe_load(f)
except FileNotFoundError:
    pytest.fail("Schema file order.yaml not found.")
except Exception as e:
    pytest.fail(f"Error loading schema order.yaml: {e}")


# Test passing good sample case
def test_passing_good_sample():
    file_path = f"./{dataFolder}/goodSample.json"
    try:
        with open(file_path, "r") as f:
            goodItem = json.load(f)
    except FileNotFoundError:
        pytest.fail(f"Test data file not found: {file_path}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Error decoding JSON from {file_path}: {e}")

    try:
        jsonschema.validate(instance=goodItem, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Validation failed unexpectedly for {file_path}: {e}")


# Test passing order2 sample case
def test_passing_order2_sample():
    file_path = f"./{dataFolder}/order2.yaml"
    try:
        with open(file_path, "r") as f:
            order2Item = yaml.safe_load(f)
    except FileNotFoundError:
        pytest.fail(f"Test data file not found: {file_path}")
    except yaml.YAMLError as e:
        pytest.fail(f"Error decoding YAML from {file_path}: {e}")

    try:
        jsonschema.validate(instance=order2Item, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Validation failed unexpectedly for {file_path}: {e}")


# Test bad case: wrong type
def test_wrong_type():
    file_path = f"./{dataFolder}/wrongType.json"
    try:
        with open(file_path, "r") as f:
            badItem = json.load(f)
    except FileNotFoundError:
        pytest.fail(f"Test data file not found: {file_path}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Error decoding JSON from {file_path}: {e}")

    with pytest.raises(ValidationError):
        jsonschema.validate(instance=badItem, schema=schema)


# Test bad case: extraneous column
# (Removing this test as additionalProperties is now allowed at the root)
# def test_extra_column():
#     file_path = f"./{dataFolder}/extraCol.json"
#     try:
#         with open(file_path, "r") as f:
#             badItem = json.load(f)
#     except FileNotFoundError:
#         pytest.fail(f"Test data file not found: {file_path}")
#     except json.JSONDecodeError as e:
#         pytest.fail(f"Error decoding JSON from {file_path}: {e}")
#
#     # Expect validation to fail because root additionalProperties is false
#     with pytest.raises(ValidationError) as excinfo:
#         jsonschema.validate(instance=badItem, schema=schema)
#     # Optionally check the specific error message if needed
#     # assert "Additional properties are not allowed" in str(excinfo.value)
