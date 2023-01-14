"""Interface for Avro Drivers."""

from io import BufferedIOBase
from typing import TYPE_CHECKING, Protocol, Type, TypeVar

if TYPE_CHECKING:
    from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject

S = TypeVar("S", bound="AbstractNeoGenObject")  # noqa: VNE001 - Type variable.


class AvroDriverType(Protocol):
    """Avro data driver type Protocol."""

    def read(self, schema: Type[S], source: BufferedIOBase) -> S:
        """Read a single schema from source stream and return a typed instance."""
        ...

    def write(self, schema: S, target: BufferedIOBase) -> None:
        """Write a single schema to target stream."""
        ...
