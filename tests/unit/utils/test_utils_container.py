"""Tests for utils.container."""

import pytest

import fromconfig


@pytest.mark.parametrize(
    "obj, expected",
    [
        pytest.param([], False, id="list"),
        pytest.param((), False, id="tuple"),
        pytest.param({}, True, id="dict"),
        pytest.param(fromconfig.utils.WeakImmutableDict(), True, id="weak-immutable-dict"),
        pytest.param(fromconfig.Config(), True, id="Config"),
    ],
)
def test_utils_is_mapping(obj, expected):
    """Test utils.is_mapping."""
    assert fromconfig.utils.is_mapping(obj) == expected


@pytest.mark.parametrize(
    "obj, expected",
    [
        pytest.param([], True, id="list"),
        pytest.param({}, False, id="dict"),
        pytest.param("hello", False, id="string"),
        pytest.param((), True, id="tuple"),
    ],
)
def test_utils_is_iterable(obj, expected):
    """Test utils.is_iterable."""
    assert fromconfig.utils.is_iterable(obj) == expected


@pytest.mark.parametrize(
    "cls, default_cls, args, kwargs, expected",
    [
        pytest.param(dict, None, [{1: 2}], {}, {1: 2}, id="dict+none"),
        pytest.param(None, dict, [{1: 2}], {}, {1: 2}, id="none+dict"),
        pytest.param(dict, dict, [{1: 2}], {}, {1: 2}, id="dict+dict"),
        pytest.param(list, None, [[1]], {}, [1], id="list+none"),
        pytest.param(None, list, [[1]], {}, [1], id="none+list"),
        pytest.param(list, list, [[1]], {}, [1], id="list+list"),
        pytest.param(tuple, None, [[1]], {}, (1,), id="tuple+none"),
        pytest.param(None, tuple, [[1]], {}, (1,), id="none+tuple"),
        pytest.param(tuple, tuple, [[1]], {}, (1,), id="tuple+tuple"),
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
