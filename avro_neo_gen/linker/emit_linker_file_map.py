"""Write a linker file map to disk."""

import ast
from pathlib import Path
from typing import Union

from avro_neo_gen.type_defs import LinkerFileMap


def emit_linker_file_map(linker_file_map: LinkerFileMap, base_path: Union[str, Path] = "./build") -> None:
    """Write a linker file map to disk.

    :param linker_file_map: Linker file map to commit to disk.
    :type linker_file_map: :class:`LinkerFileMap`
    :param base_path: Base path to write generated files and directories.
    :type base_path: Union[str, :class:`pathlib.Path`]
    """
    base_path = Path(base_path)
    for filename, module in linker_file_map.items():
        file_path = base_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(ast.unparse(module) + "\n", encoding="utf-8")
