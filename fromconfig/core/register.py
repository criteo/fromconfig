"""Register."""

from fromconfig.utils import import_from_string, ImmutableDict


class _Register(ImmutableDict):
    """Register."""

    def __call__(self, name: str, attr=None):
        """Return decorator that register an attribute."""

        def _decorator(attr):
            self[name] = attr
            return attr

        return _decorator if attr is None else _decorator(attr)

    def resolve(self, name: str, safe: bool = True):
        """Resolve attribute from register or import string.

        Parameters
        ----------
        name : str
            Attribute name, can be either register key or import string
        safe : bool, optional
            If True, don't use import strings
        """
        if name in self:
            return self[name]
        if not safe:
            return import_from_string(name)
        else:
            raise ValueError(f"Attribute {name} not found in register")


register = _Register()
