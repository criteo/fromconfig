"""Tests for utils.container."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "obj, expected",
    [([], False), ((), False), ({}, True), (fromconfig.utils.WeakImmutableDict(), True), (fromconfig.Config(), True)],
)
def test_utils_is_mapping(obj, expected):
    """Test utils.is_mapping."""
    assert fromconfig.utils.is_mapping(obj) == expected


@pytest.mark.parametrize("obj, expected", [([], True), ({}, False), ("hello", False), ((), True)])
def test_utils_is_iterable(obj, expected):
    """Test utils.is_iterable."""
    assert fromconfig.utils.is_iterable(obj) == expected


@pytest.mark.parametrize(
    "cls, default_cls, args, kwargs, expected",
    [
        (dict, None, [{1: 2}], {}, {1: 2}),
        (None, dict, [{1: 2}], {}, {1: 2}),
        (dict, dict, [{1: 2}], {}, {1: 2}),
        (list, None, [[1]], {}, [1]),
        (None, list, [[1]], {}, [1]),
        (list, list, [[1]], {}, [1]),
        (tuple, None, [[1]], {}, (1,)),
        (None, tuple, [[1]], {}, (1,)),
        (tuple, tuple, [[1]], {}, (1,)),
    ],
)
def test_utils_try_init(cls, default_cls, args, kwargs, expected):
    """Test utils.try_init."""
    assert fromconfig.utils.try_init(cls, default_cls, *args, **kwargs) == expected


def test_utils_weak_immutable_dict():
    """Test utils.WeakImmutableDict."""
    d = fromconfig.utils.WeakImmutableDict()
    d[1] = 2
    assert fromconfig.utils.is_mapping(d)
    assert dict(d) == {1: 2}
    with pytest.raises(KeyError):
        d[1] = 1
