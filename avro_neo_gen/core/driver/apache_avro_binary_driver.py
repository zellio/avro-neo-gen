"""Driver impl. using the Apache Avro python library."""

import json
from io import BufferedIOBase
from typing import TYPE_CHECKING, Type, TypeVar

import avro.io
import avro.schema

from avro_neo_gen.core.driver.abstract_avro_driver import AbstractAvroDriver

if TYPE_CHECKING:
    from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject

__all__ = ["ApacheAvroBinaryDriver"]


S = TypeVar("S", bound="AbstractNeoGenObject")  # noqa: VNE001 - Type variable.


class ApacheAvroBinaryDriver(AbstractAvroDriver):
    """Driver impl. using the Apache Avro python library."""

    def read(self, schema_type: Type[S], source: BufferedIOBase) -> S:
        """Read a single schema from source stream and return a typed instance.

        :param schema_type:
        :type schema_type: Type[S]
        :return:
        :rtype: S
        """
        avro_schema = avro.schema.parse(json.dumps(schema_type.__canonical_schema__))
        datum_reader = avro.io.DatumReader(writers_schema=avro_schema, readers_schema=avro_schema)
        datum = datum_reader.read(decoder=avro.io.BinaryDecoder(reader=source))
        return schema_type.decode(datum)

    def write(self, schema: S, target: BufferedIOBase) -> None:
        """Write a single schema to target stream.

        :param schema_type:
        :type schema_type: S
        """
        avro_schema = avro.schema.parse(schema.canonical_schema_json)
        datum_writer = avro.io.DatumWriter(writers_schema=avro_schema)
        datum_writer.write(datum=schema.encode(), encoder=avro.io.BinaryEncoder(writer=target))
