"""Link corelib files."""

import ast
from pathlib import Path

from avro_neo_gen.type_defs import LinkerFileMap


def link_corelib() -> LinkerFileMap:
    """Generate a file map of the current corelib.

    :return: File map of the current corelib files.
    :rtype: ``avro_neo_gen.type_defs.LinkerFileMap``
    """
    lib_path = Path(__file__).absolute().parent.parent.parent
    corelib_path = lib_path / "avro_neo_gen" / "core"
    ignored_file_names = ("shim.py",)
    corelib_files = (
        corelib_file.relative_to(corelib_path)
        for corelib_file in corelib_path.glob("**/*.py")
        if corelib_file.name not in ignored_file_names
    )

    return {
        str(corelib_file): ast.parse((corelib_path / corelib_file).read_text(encoding="utf-8"))
        for corelib_file in corelib_files
    }
