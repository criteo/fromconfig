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
        ("A", CustomEnum.A),
        ("B", CustomEnum.B),
        ("C", ValueError),
        (CustomEnum.A, CustomEnum.A),
        (CustomEnum.B, CustomEnum.B),
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
        ("A", CustomEnum.A, True),
        ("B", CustomEnum.B, True),
        ("A", CustomEnum.B, False),
        ("B", CustomEnum.A, False),
        ("C", CustomEnum.B, False),
        (CustomEnum.A, CustomEnum.A, True),
        (CustomEnum.B, CustomEnum.B, True),
        (CustomEnum.A, CustomEnum.B, False),
        (CustomEnum.B, CustomEnum.A, False),
    ],
)
def test_utils_strenum_equality(left, right, expected):
    """Test utils.strenum equality."""
    assert (left == right) == expected


@pytest.mark.parametrize(
    "member, expected", [("A", True), ("B", True), ("C", False), (CustomEnum.A, True), (CustomEnum.B, True)]
)
def test_utils_strenum_membership(member, expected):
    """Test utils.strenum membership."""
    assert (member in CustomEnum) == expected
