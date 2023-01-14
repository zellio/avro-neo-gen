"""Link compiled namespace map into final module file map."""

from pathlib import Path

from avro_neo_gen.linker.inject_corelib_sys_path_shim import (
    inject_corelib_sys_path_shim,
)
from avro_neo_gen.linker.link_compiler_namespace_map import link_compiler_namespace_map
from avro_neo_gen.linker.link_corelib import link_corelib
from avro_neo_gen.type_defs import CompilerNamespaceMap, LinkerFileMap


def link_module(namespace_map: CompilerNamespaceMap) -> LinkerFileMap:
    """Link compiled namespace map into final module file map.

    :param namespace_map: Source compiled namespace map to link and join with corelib.
    :type namespace_map: :class:`CompilerNamespaceMap`
    :return: Final linked namepsace map for emitting to disk.
    :rtype: :class:`LinkerFileMap`
    """
    corelib_linker_file_map = link_corelib()
    generated_linker_file_map = link_compiler_namespace_map(namespace_map)
    injected_linker_file_map = inject_corelib_sys_path_shim(generated_linker_file_map)
    return injected_linker_file_map | {
        str(Path("avro_neo_gen") / "core" / path): ast for path, ast in corelib_linker_file_map.items()
    }
