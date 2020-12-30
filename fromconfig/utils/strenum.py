"""String Enum."""

from enum import Enum, EnumMeta


class StrEnumMeta(EnumMeta):
    """Meta class for String Enum."""

    # pylint: disable=unsupported-membership-test,not-an-iterable

    def __contains__(cls, member):
        return any(key == member for key in cls)


class StrEnum(str, Enum, metaclass=StrEnumMeta):
    """String Enum."""
