"""Generated RecordSchema base class."""

from typing import Any, Type, TypeVar

from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject
from avro_neo_gen.core.type_defs import AvroRecordTypeDef

NeoGenRecordDatum = dict[str, Any]
Self = TypeVar("Self", bound="NeoGenRecord")


class NeoGenRecord(AbstractNeoGenObject):
    """Generated RecordSchema base class."""

    __schema__: AvroRecordTypeDef

    def __init__(self) -> None:
        """Construct default instance.

        NB. This is designed to be overwritten.
        """
        self._datum: dict[str, Any] = {}

    def __repr__(self) -> str:
        """Repr instance."""
        return f"<{self.__class__.__name__}(datum={self.encode()})>"

    def encode(self) -> NeoGenRecordDatum:
        """Encode record as avro json."""
        return {
            key: value.encode() if isinstance(value, AbstractNeoGenObject) else value
            for key, value in self._datum.items()
        }

    @classmethod
    def decode(cls: Type[Self], datum: NeoGenRecordDatum) -> Self:
        """Ingest datum to internal state, munging based on spec."""
        return cls(**datum)
