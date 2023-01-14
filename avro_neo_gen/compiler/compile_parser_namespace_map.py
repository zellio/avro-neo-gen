"""Compile parser namespace map."""

import contextlib
from ast import AST

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema import compile_avro_schema
from avro_neo_gen.type_defs import (
    CompilerNamespaceMap,
    CompilerNamespaceMapCell,
    ParserNamespaceMap,
)


def compile_parser_namespace_map(namespace_map: ParserNamespaceMap) -> CompilerNamespaceMap:
    """Compile parser namespace map.

    :return: CompilerNamespaceMap
    :rtype: :class:`CompilerNamespaceMap`
    """

    def _safe_compile(avro_schema: AvroSchema) -> list[AST]:
        with contextlib.suppress(NotImplementedError):
            return compile_avro_schema(avro_schema)
        return []

    return {
        namespace: [CompilerNamespaceMapCell(schema=schema, ast=_safe_compile(schema)) for schema in schemas]
        for namespace, schemas in namespace_map.items()
    }
