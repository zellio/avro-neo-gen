"""Inject corelib sys path loader shim."""

import ast
from inspect import cleandoc

from avro_neo_gen.type_defs import LinkerFileMap


def inject_corelib_sys_path_shim(linker_file_map: LinkerFileMap) -> LinkerFileMap:
    """Inject corelib sys path loader shim.

    :param linker_file_map:
    :type linker_file_map: LinkerFileMap
    :return: Updated :class:`LinkerPathMap` with the inject loader shim.
    :rtype: :class:`LinkerPathMap`

    On load, the corelib updates Python's module path to include the root of
    the generated source tree. This is done so the ``avro_neo_gen.core``
    namespace can be properly loaded.

    .. highlight:: python
    .. code-block::

        # Loader shim

        import sys
        import pathlib

        lib_path = pathlib.Path(__file__).absolute().parent
        if lib_path not in sys.path:
            sys.path.append(str(lib_path))
    """
    loader_shim_ast = ast.parse(
        cleandoc(
            """
        import sys
        import pathlib

        lib_path = pathlib.Path(__file__).absolute().parent
        if lib_path not in sys.path:
            sys.path.append(str(lib_path))
    """
        )
    )
    current_module = linker_file_map.get("__init__.py", ast.Module(type_ignores=[], body=[]))
    current_module.body = [
        *loader_shim_ast.body,
        *current_module.body,
    ]

    return linker_file_map | {"__init__.py": current_module}
