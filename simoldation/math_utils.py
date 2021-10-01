"""Math utilities for the simulation."""

from typing import List, Tuple


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


def apply_pbcs(index: int, boundary: int) -> int:
    """Applies periodic boundary conditions (PBCs).

    Args:
        index (int): Index to apply the PBCs to
        boundary (int): Length of the boundary

    Returns:
        int: Index with PBCs applied to it
    """
    if index < 0:
        index += boundary
    elif index >= boundary:
        index -= boundary

    return index


def _get_neighbors(x: int, y: int, dataset: List[List[float]]) -> List[Tuple[int, int]]:
    """Gets the neighbors of dataset[y][x] in a 3x3 kernel.

    Args:
        x (int): Row
        y (int): Column
        dataset (list of lists): A 2D list representing the dataset

    Returns:
        list of tuples: Each tuple contains indices of a particular neighbor
    """
    width = len(dataset[0])
    height = len(dataset)

    # These hacks ensure that we don't throw an index error.
    if x == width - 1:
        x = -1
    if y == height - 1:
        y = -1

    neighbors = []
    neighbors.extend(
        [
            dataset[y - 1][x - 1],
            dataset[y - 1][x],
            dataset[y - 1][x + 1],
            dataset[y][x - 1],
            dataset[y][x + 1],
            dataset[y + 1][x - 1],
            dataset[y + 1][x],
            dataset[y + 1][x + 1],
        ]
    )

    return neighbors


def apply_mean_filter(indices: Tuple[int, int], dataset: List[List[float]]):
    """Applies mean filter to the value at given `indices`.

    Args:
        indices (tuple): Indices of the value to apply the mean filter to
        dataset (list of lists): A 2D list representing the dataset

    Returns:
        float: Value after applying the mean filter"""
    neighbors = _get_neighbors(*indices, dataset)

    x, y = indices
    value_to_mean_filter = dataset[y][x]

    return (value_to_mean_filter + sum(neighbors)) / (len(neighbors) + 1)
