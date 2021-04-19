"""Test for utils.nest."""

import copy
import numbers
from functools import partial
import pytest

import fromconfig


@pytest.mark.parametrize(
    "config, expected",
    [
        pytest.param({"x": 1}, [("x", 1)]),
        pytest.param({"x": {"y": 1}}, [("x.y", 1)]),
        pytest.param({"x": [1]}, [("x[0]", 1)]),
    ],
)
def test_utils_flatten_expand(config, expected):
    """Test utils.flatten."""
    assert fromconfig.utils.flatten(config) == expected
    assert fromconfig.utils.expand(expected) == config


@pytest.mark.parametrize("config", [pytest.param({"a.b": {"c": "d"}}, id="key-has-dot")])
def test_utils_flatten_impossible(config):
    with pytest.raises(ValueError):
        fromconfig.utils.flatten(config)


@pytest.mark.parametrize(
    "item1, item2, expected",
    [
        pytest.param({"x": 1}, {"y": 2}, {"x": 1, "y": 2}, id="simple"),
        pytest.param({"x": 1}, {"x": 2}, {"x": 2}, id="override"),
    ],
)
def test_utils_merge_dict(item1, item2, expected):
    """Test utils.merge_dict."""
    assert fromconfig.utils.merge_dict(item1, item2, allow_override=True) == expected


@pytest.mark.parametrize(
    "item1, item2, allow_override, error",
    [pytest.param({"x": 1}, [1], True, TypeError), pytest.param({"x": 1}, {"x": 2}, False, ValueError)],
)
def test_utils_merge_dict_errors(item1, item2, allow_override, error):
    with pytest.raises(error):
        fromconfig.utils.merge_dict(item1, item2, allow_override=allow_override)


def inc(item, value):
    """Increment item with value if item is Number."""
    if isinstance(item, numbers.Number):
        return item + value
    return item


@pytest.mark.parametrize(
    "map_fn, item, expected",
    [
        pytest.param(partial(inc, value=1), 1, 2, id="int"),
        pytest.param(partial(inc, value=1), [1], [2], id="list"),
        pytest.param(partial(inc, value=1), {"x": 1}, {"x": 2}, id="dict"),
        pytest.param(partial(inc, value=1), {"x": [1]}, {"x": [2]}, id="dict+list"),
        pytest.param(partial(inc, value=1), {"x": {"y": 1}}, {"x": {"y": 2}}, id="dict+dict"),
        pytest.param(partial(inc, value=1), "a", "a", id="string"),
        pytest.param(partial(inc, value=1), {"x": 1, "a": "a"}, {"x": 2, "a": "a"}, id="dict+string"),
    ],
)
def test_utils_depth_map(map_fn, item, expected):
    """Test utils.depth_map."""
    original = copy.deepcopy(item)
    got = fromconfig.utils.depth_map(map_fn, item)
    assert got == expected, f"{got} != {expected}"
    assert original == item, "depth_map should not mutate"
