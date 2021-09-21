"""Tests for the `math_utils.py` module."""

import pytest
from simoldation.math_utils import normalize_to_range


normalize_to_range_parameters = (
    "test_value",
    "test_range",
    "test_dataset_lower_bound",
    "test_dataset_upper_bound",
    "expected",
)
normalize_to_range_test_data = [
    (0, (0, 1), 0, 1920, 0),
    (960, (0, 1), 0, 1920, 0.5),
    (1920, (0, 1), 0, 1920, 1),
]


@pytest.mark.parametrize(
    normalize_to_range_parameters,
    normalize_to_range_test_data,
)
def test_normalize_to_range(
    test_value, test_range, test_dataset_lower_bound, test_dataset_upper_bound, expected
):
    """Tests the `normalize_to_range` function."""

    assert (
        normalize_to_range(
            test_value, test_range, test_dataset_lower_bound, test_dataset_upper_bound
        )
        == expected
    )
