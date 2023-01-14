"""Abstract base class for all Avro Drivers."""

from abc import ABC, abstractmethod
from io import BufferedIOBase
from typing import TYPE_CHECKING, Type, TypeVar

from avro_neo_gen.core.driver.avro_driver_type import AvroDriverType

if TYPE_CHECKING:
    from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject

S = TypeVar("S", bound="AbstractNeoGenObject")  # noqa: VNE001 - Type variable.


class AbstractAvroDriver(ABC, AvroDriverType):
    """Abstract base class for all Avro Drivers."""

    @abstractmethod
    def read(self, schema_type: Type[S], source: BufferedIOBase) -> S:
        """Read a single schema from source stream and return a typed instance."""
        raise NotImplementedError

    @abstractmethod
    def write(self, schema: S, target: BufferedIOBase) -> None:
        """Write a single schema to target stream."""
        raise NotImplementedError
