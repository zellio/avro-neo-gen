"""Generated Avro NeoGen type Protocol."""

from collections import OrderedDict
from typing import Any, Protocol

from avro_neo_gen.core.type_defs import AvroSchemaTypeAlias


class NeoGenType(Protocol):
    """Generated Avro NeoGen type Protocol."""

    __canonical_schema__: OrderedDict[str, Any]
    __schema__: AvroSchemaTypeAlias

    @property
    def canonical_schema(self) -> OrderedDict[str, Any]:
        """Avro canonical schema."""
        ...

    @property
    def canonical_schema_json(self) -> str:
        """Avro canonical schema encoded as json string."""
        ...

    @property
    def schema(self) -> AvroSchemaTypeAlias:
        """Avro schema."""
        ...

    @property
    def schema_json(self) -> str:
        """Avro schema encoded as json string."""
        ...
