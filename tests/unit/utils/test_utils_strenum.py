"""Tests for utils.strenum."""

import pytest

import fromconfig


class CustomEnum(fromconfig.utils.StrEnum):
    """Custom Enum."""

    A = "A"
    B = "B"


@pytest.mark.parametrize(
    "before, after",
    [
        pytest.param("A", CustomEnum.A, id="stringA+enumA"),
        pytest.param("B", CustomEnum.B, id="stringB+enumB"),
        pytest.param("C", ValueError, id="stringC"),
        pytest.param(CustomEnum.A, CustomEnum.A, id="enumA+enumA"),
        pytest.param(CustomEnum.B, CustomEnum.B, id="enumB+enumB"),
    ],
)
def test_utils_strenum_resolution(before, after):
    """Test utils.strenum resolution."""
    if isinstance(after, CustomEnum):
        assert CustomEnum(before) is after  # "is" stronger than ==
    else:
        with pytest.raises(after):
            CustomEnum(before)


@pytest.mark.parametrize(
    "left, right, expected",
    [
        pytest.param("A", CustomEnum.A, True, id="stringA+enumA"),
        pytest.param("B", CustomEnum.B, True, id="stringB+enumB"),
        pytest.param("A", CustomEnum.B, False, id="stringA+enumB"),
        pytest.param("B", CustomEnum.A, False, id="stringB+enumA"),
        pytest.param("C", CustomEnum.A, False, id="stringC+enumA"),
        pytest.param("C", CustomEnum.B, False, id="stringC+enumB"),
        pytest.param(CustomEnum.A, CustomEnum.A, True, id="enumA+enumA"),
        pytest.param(CustomEnum.B, CustomEnum.B, True, id="enumB+enumB"),
        pytest.param(CustomEnum.A, CustomEnum.B, False, id="enumA+enumB"),
        pytest.param(CustomEnum.B, CustomEnum.A, False, id="enumB+enumA"),
    ],
)
def test_utils_strenum_equality(left, right, expected):
    """Test utils.strenum equality."""
    assert (left == right) == expected


@pytest.mark.parametrize(
    "member, expected",
    [
        pytest.param("A", True, id="stringA"),
        pytest.param("B", True, id="stringB"),
        pytest.param("C", False, id="stringC"),
        pytest.param(CustomEnum.A, True, id="enumA"),
        pytest.param(CustomEnum.B, True, id="enumB"),
    ],
)
def test_utils_strenum_membership(member, expected):
    """Test utils.strenum membership."""
    assert (member in CustomEnum) == expected
