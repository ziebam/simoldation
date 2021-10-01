"""Tests for the `math_utils.py` module."""

import pytest
from simoldation.math_utils import apply_mean_filter, normalize_to_range, apply_pbcs


@pytest.mark.parametrize(
    (
        "test_value",
        "test_range",
        "test_dataset_lower_bound",
        "test_dataset_upper_bound",
        "expected",
    ),
    [
        (0, (0, 1), 0, 1920, 0),
        (960, (0, 1), 0, 1920, 0.5),
        (1920, (0, 1), 0, 1920, 1),
    ],
)
def test_normalize_to_range(
    test_value, test_range, test_dataset_lower_bound, test_dataset_upper_bound, expected
):
    assert (
        normalize_to_range(
            test_value, test_range, test_dataset_lower_bound, test_dataset_upper_bound
        )
        == expected
    )


@pytest.mark.parametrize(
    ("test_value", "test_boundary", "expected"),
    [(-1, 100, 99), (100, 100, 0), (-10, 100, 90), (110, 100, 10)],
)
def test_apply_pbcs(test_value, test_boundary, expected):
    assert apply_pbcs(test_value, test_boundary) == expected


@pytest.mark.parametrize(
    ("test_indices", "test_dataset", "expected"),
    [
        ((0, 0), [[5.0, 3.0, 6.0], [2.0, 1.0, 9.0], [8.0, 4.0, 7.0]], 5.0),
        ((1, 0), [[5.0, 3.0, 6.0], [2.0, 1.0, 9.0], [8.0, 4.0, 7.0]], 5.0),
        ((1, 1), [[5.0, 3.0, 6.0], [2.0, 1.0, 9.0], [8.0, 4.0, 7.0]], 5.0),
        ((0, 0), [[6.0, 2.0, 0.0], [3.0, 97.0, 4.0], [19.0, 3.0, 10.0]], 16.0),
        ((1, 0), [[6.0, 2.0, 0.0], [3.0, 97.0, 4.0], [19.0, 3.0, 10.0]], 16.0),
        ((1, 1), [[6.0, 2.0, 0.0], [3.0, 97.0, 4.0], [19.0, 3.0, 10.0]], 16.0),
    ],
)
def test_apply_mean_filter(test_indices, test_dataset, expected):
    assert apply_mean_filter(test_indices, test_dataset) == expected
