"""String Enum."""

from enum import Enum, EnumMeta


class StrEnumMeta(EnumMeta):
    """Meta class for String Enum."""

    # pylint: disable=unsupported-membership-test,not-an-iterable

    def __contains__(cls, member):
        if isinstance(member, str):
            return any(key == member for key in cls)
        return member in cls


class StrEnum(str, Enum, metaclass=StrEnumMeta):
    """String Enum."""
