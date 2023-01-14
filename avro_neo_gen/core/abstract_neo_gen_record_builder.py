"""Generated RecordSchemaBuilder abstract class."""

from abc import ABC, abstractmethod
from typing import Any

from avro_neo_gen.core.neo_gen_builder import NeoGenBuilder
from avro_neo_gen.core.neo_gen_record import NeoGenRecord


class AbstractNeoGenRecordBuilder(ABC, NeoGenBuilder):
    """Generated RecordSchemaBuilder abstract class."""

    def __init__(self) -> None:
        """Concrete shared constructor."""
        self._state: dict[str, Any] = {}

    @abstractmethod
    def build(self) -> NeoGenRecord:
        """Build the builder target class."""
        raise NotImplementedError
