"""Internal type defs."""

from ast import AST, Module
from typing import Optional, TypedDict

from avro_neo_gen.avro_schema import AvroSchema

ParserNamespaceMap = dict[str, list[AvroSchema]]


class CompilerNamespaceMapCell(TypedDict):
    """Internal data class for compiler namespace.

    Contains the schema and compiled AST for the schema. Namespace is gathered
    from the parent key of the list containing the cell in the namespace map.
    """

    schema: AvroSchema
    ast: Optional[list[AST]]


CompilerNamespaceMap = dict[str, list[CompilerNamespaceMapCell]]


ModuleImports = dict[str, set]


LinkerRequiredImports = dict[str, set[str]]


LinkerFileMap = dict[str, Module]
