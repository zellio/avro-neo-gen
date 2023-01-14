"""Unroll Avro schemas into their calculated namespaces."""

from typing import Iterable, Iterator

from avro.schema import Schema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.type_defs import ParserNamespaceMap
from avro_neo_gen.utils import dict_func_reduce, flat_map


def _build_namespace_map(avro_schema: AvroSchema[Schema], namespace: str = ".") -> Iterator[ParserNamespaceMap]:
    schema: AvroSchema[Schema]
    for schema in avro_schema:
        yield from _build_namespace_map(schema, avro_schema.namespace or namespace)
    yield {avro_schema.namespace or namespace: [avro_schema]}


def parse_schema(schemas: Iterable[Schema]) -> ParserNamespaceMap:
    """Expand Avro schemas and their contained types into a namespace map.

    :param schemas: Avro schemas to be parsed.
    :type schemas: Iterable[:class:`avro.schema.Schema`]
    :return: Namespace maping of schemas.
    :type: :class:`ParserNamespaceMap`
    """
    return dict_func_reduce(
        list.__add__, flat_map(lambda schema: list(_build_namespace_map(schema, ".")), map(AvroSchema, schemas))
    )
