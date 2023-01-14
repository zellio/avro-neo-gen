import ast
from pathlib import Path

from avro_neo_gen.linker.link_corelib import link_corelib


class TestLinkerLinkCorelib:
    def test_link_corelib(self) -> None:
        lib_path = Path(__file__).absolute().parent.parent
        corelib_path = lib_path / "avro_neo_gen" / "core"
        ignored_file_names = ("shim.py",)
        corelib_files = (
            str(corelib_file.relative_to(corelib_path))
            for corelib_file in corelib_path.glob("**/*.py")
            if corelib_file.name not in ignored_file_names
        )

        corelib_linker_file_map = link_corelib()

        for corelib_file in corelib_files:
            assert corelib_file in corelib_linker_file_map
            source_python = ast.unparse(ast.parse((corelib_path / corelib_file).read_text(encoding="utf-8")))
            assert source_python == ast.unparse(corelib_linker_file_map[corelib_file])
