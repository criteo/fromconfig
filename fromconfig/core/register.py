"""Register."""

from collections.abc import MutableMapping

from fromconfig.utils import import_from_string


class _Register(MutableMapping):
    """Register."""

    def __init__(self):
        self._register = {}

    def __getitem__(self, item):
        return self._register[item]

    def __setitem__(self, key, value):
        if key in self._register:
            raise KeyError(f"Key {key} already in {self}. You must delete it first.")
        self._register[key] = value

    def __delitem__(self, key):
        self._register.__delitem__(key)

    def __iter__(self):
        yield from self._register

    def __len__(self):
        return len(self._register)

    def __call__(self, name: str, attr=None):
        """Return decorator that register an attribute."""

        def _decorator(attr):
            self[name] = attr
            return attr

        return _decorator if attr is None else _decorator(attr)

    def resolve(self, name: str, safe: bool = False):
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
