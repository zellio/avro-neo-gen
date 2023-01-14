"""Link compiler namespace map into a linker file map."""

from ast import ImportFrom, Module, alias
from pathlib import Path
from typing import Iterable

from avro_neo_gen.linker.avro_schema_required_imports import (
    avro_schema_required_imports,
)
from avro_neo_gen.type_defs import (
    CompilerNamespaceMap,
    CompilerNamespaceMapCell,
    LinkerFileMap,
)
from avro_neo_gen.utils import dict_func_reduce, flat_map


def _link_map_entry(cells: Iterable[CompilerNamespaceMapCell]) -> Module:
    """Determine requirements for a schema and link the AST.

    :param cells: Internal :class:`CompilerNamespaceMap` list of cells containing
        avro schemas and compiled AST
    :type cells: Iterable[:class:`CompilerNamespaceMapCell`]
    :return: Fully linked python AST for exporting
    :rtype: :class:`ast.Module`
    """
    sorted_cells = sorted(cells, key=lambda cell: cell["schema"].name or "")
    schemas = (cell["schema"] for cell in sorted_cells)
    required_imports = dict_func_reduce(set.union, map(avro_schema_required_imports, schemas))
    required_imports_ast = (
        ImportFrom(
            module=module,
            names=[alias(name=name) for name in sorted(required_imports[module])],
            level=0,
        )
        for module in sorted(required_imports.keys())
    )

    return Module(
        body=[
            *required_imports_ast,
            *(flat_map(lambda cell: cell["ast"] or [], cells)),
        ],
        type_ignores=[],
    )


def link_compiler_namespace_map(compiler_namespace_map: CompilerNamespaceMap) -> LinkerFileMap:
    """Link compiler namespace map into a linker file map.

    :param compiler_namespace_map: Compiler namespace map to link.
    :type compiler_namespace_map: CompilerNamespaceMap
    :return: Linked namespace map ready for merging with corelib.
    :rtype: :class:`avro_neo_gen.type_defs.LinkerFileMap`
    """
    path_base = Path("")
    return {
        str(path_base.joinpath(*namespace.split(".")) / "__init__.py"): _link_map_entry(cells)
        for namespace, cells in compiler_namespace_map.items()
    }
