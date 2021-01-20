"""Register."""

from fromconfig.utils import from_import_string, WeakImmutableDict


class _Register(WeakImmutableDict):
    """Register python classes and functions by name.

    Examples
    --------
    >>> from fromconfig.core.register import _Register
    >>> register = _Register()
    >>> @register("my_function")
    ... def my_function():
    ...     print("Hello world!")
    >>> register.resolve("my_function") == my_function
    True
    """

    def __call__(self, name: str, attr=None):
        """Register attr under name name or return decorator."""

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
            return from_import_string(name)
        else:
            raise ValueError(f"Attribute {name} not found in register")


register = _Register()
