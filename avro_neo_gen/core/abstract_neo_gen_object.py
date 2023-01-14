"""Generated type abstract class."""

import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from io import BufferedIOBase
from typing import Any, Type, TypeVar

from avro_neo_gen.core.driver.driver_proxy import DriverProxy
from avro_neo_gen.core.neo_gen_encodable import NeoGenEncodable
from avro_neo_gen.core.neo_gen_type import NeoGenType
from avro_neo_gen.core.type_defs import AvroSchemaTypeAlias

__all__ = ["AbstractNeoGenObjectMeta", "AbstractNeoGenObject"]

Self = TypeVar("Self", bound="AbstractNeoGenObject")


class AbstractNeoGenObject(ABC, NeoGenType, NeoGenEncodable):
    """Generated type abstract class."""

    __canonical_schema__: OrderedDict[str, Any]
    __schema__: AvroSchemaTypeAlias
    __driver_proxy__ = DriverProxy()

    @abstractmethod
    def __init__(self, datum: Any) -> None:
        """Abstract constructor."""
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Abstract __repr___."""
        raise NotImplementedError

    @property
    def canonical_schema(self) -> OrderedDict[str, Any]:
        """Avro canonical schema."""
        return self.__class__.__canonical_schema__

    @property
    def canonical_schema_json(self) -> str:
        """Avro canonical schema encoded as json string."""
        return json.dumps(self.canonical_schema)

    @property
    def schema(self) -> AvroSchemaTypeAlias:
        """Avro schema."""
        return self.__class__.__schema__

    @property
    def schema_json(self) -> str:
        """Avro schema encoded as json string."""
        return json.dumps(self.schema)

    @classmethod
    def read(cls: Type[Self], source: BufferedIOBase) -> Self:
        """Read encoded avro schema via DriverProxy into a new typed instance."""
        return cls.__driver_proxy__.read(cls, source)

    def write(self, target: BufferedIOBase) -> None:
        """Write instance values into an  encoded avro schema via DriverProxy."""
        self.__class__.__driver_proxy__.write(self, target)

    @abstractmethod
    def encode(self) -> Any:
        """Cast typed entity to representational data per caonical_schema."""
        raise NotImplementedError

    def encode_json(self) -> str:
        """Encode self.encode as json string."""
        return json.dumps(self.encode())

    @classmethod
    @abstractmethod
    def decode(cls: Type[Self], datum: Any) -> Self:
        """Ingest datum to internal state, munging based on spec."""
        raise NotImplementedError

    @classmethod
    def decode_json(cls: Type[Self], datum: str) -> Self:
        """Decode datum as a json string."""
        return cls.decode(json.loads(datum))


AbstractNeoGenObjectMeta: type = type(AbstractNeoGenObject)
