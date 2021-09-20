"""Math utilities for the simulation."""

from typing import Tuple


def normalize_to_range(
    value: float,
    _range: Tuple[float, float],
    dataset_lower_bound: float,
    dataset_upper_bound: float,
) -> float:
    """Normalizes the `value` to a given `_range`.

    Args:
        value (float): The value to normalize
        _range (tuple): Target range for the normalization
        dataset_lower_bound (float): Lower bound of the dataset
        dataset_upper_bound (float): Upper bound of the dataset

    Returns:
        float: Normalized value
    """
    lower_bound, upper_bound = _range

    multiplier = upper_bound - lower_bound
    numerator = value - dataset_lower_bound
    denominator = dataset_upper_bound - dataset_lower_bound

    return multiplier * numerator / denominator + lower_bound
