"""Shared exception class defs."""


class NeoGenError(Exception):
    """Base shared error class."""

    pass


class NeoGenAttributeError(NeoGenError, AttributeError):
    """Avro NeoGen version of AttributeError."""

    pass


class NeoGenKeyError(NeoGenError, KeyError):
    """Avro NeoGen version of KeyError."""

    pass


class NeoGenValueError(NeoGenError, ValueError):
    """Avro NeoGen version of ValueError."""

    pass


class NeoGenDriverError(NeoGenError):
    """Base shared driver error class."""

    pass


class NeoGenDriverModuleNotFound(NeoGenDriverError, ModuleNotFoundError):
    """Avro NeoGen Driver version of ModuleNotFoundError."""

    pass


class NeoGenDriverClassNotFound(NeoGenDriverError, ImportError):
    """Avro NeoGen Driver version of ImportError."""

    pass


class NeoGenDriverLoadFailure(NeoGenDriverError):
    """Avro NeoGen Driver failed to load the specified driver."""

    pass


class NeoGenDriverUnloadedError(NeoGenDriverError, AttributeError):
    """Attempt to use the driver proxy without first loading a target driver."""

    pass
