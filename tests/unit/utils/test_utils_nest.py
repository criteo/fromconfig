"""Test for utils.nest."""

import copy
import numbers
from functools import partial
import pytest

import fromconfig


@pytest.mark.parametrize(
    "item, cond_fn, expected",
    [
        ("x", None, "x"),
        ({"x": 1}, None, {"x": 1}),
        ({"x": {"y": 1}}, None, {"x.y": 1}),
        ({"x": {"y": 1}, "z": 2}, None, {"x.y": 1, "z": 2}),
        ({"x": {"y": 1}}, lambda item: "y" not in item, {"x": {"y": 1}}),
    ],
)
def test_utils_flatten_dict(item, cond_fn, expected):
    """Test utils.flatten_dict."""
    assert fromconfig.utils.flatten_dict(item, cond_fn) == expected


@pytest.mark.parametrize("item1, item2, expected", [({"x": 1}, {"y": 2}, {"x": 1, "y": 2})])
def test_utils_merge_dict(item1, item2, expected):
    """Test utils.merge_dict."""
    assert fromconfig.utils.merge_dict(item1, item2) == expected


def inc(item, value):
    """Increment item with value if item is Number."""
    if isinstance(item, numbers.Number):
        return item + value
    return item


@pytest.mark.parametrize(
    "map_fn, item, expected",
    [
        (partial(inc, value=1), 1, 2),
        (partial(inc, value=1), [1], [2]),
        (partial(inc, value=1), {"x": 1}, {"x": 2}),
        (partial(inc, value=1), {"x": [1]}, {"x": [2]}),
        (partial(inc, value=1), {"x": {"y": 1}}, {"x": {"y": 2}}),
        (partial(inc, value=1), "a", "a"),
        (partial(inc, value=1), {"x": 1, "a": "a"}, {"x": 2, "a": "a"}),
    ],
)
def test_utils_depth_map(map_fn, item, expected):
    """Test utils.depth_map."""
    original = copy.deepcopy(item)
    got = fromconfig.utils.depth_map(map_fn, item)
    assert got == expected, f"{got} != {expected}"
    assert original == item, "depth_map should not mutate"
