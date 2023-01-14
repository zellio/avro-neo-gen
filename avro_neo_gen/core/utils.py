"""Public utility functions."""

import inspect
from types import FrameType
from typing import Any, Optional


def record_builder_internal(self_name: str = "cls") -> dict[str, Any]:
    """Build a Record datum dict based on the kwargs of the enclosing method.

    :params self_name: The name of the `self` argument in the enclosing method.
    :type self_name: str
    :return: :class:`avro_neo_gen.core.NeoGenRecord` instance datum dict.
    :rtype: dict[str, Any]

    .. highlight:: python

    >>> def example(**kwargs):
    ...     return record_builder_internal()
    ...
    >>> example(foo=10, bar="Hello world")
    {"foo": 10, "bar": "Hello world"}
    """
    current_frame: Optional[FrameType] = inspect.currentframe()
    if current_frame is None:
        return {}

    current_frame = current_frame.f_back
    if current_frame is None:
        return {}

    keys, _, _, values = inspect.getargvalues(current_frame)
    return {key: values[key] for key in keys if key != self_name}
