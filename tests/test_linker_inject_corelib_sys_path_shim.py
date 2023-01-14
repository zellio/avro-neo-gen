import ast
from inspect import cleandoc

from avro_neo_gen.linker.inject_corelib_sys_path_shim import (
    inject_corelib_sys_path_shim,
)


class TestInjectCorelibSysPathShim:
    def test_inject_corelib_sys_path_shim(self) -> None:
        linker_file_map = {"__init__.py": ast.Module(type_ignores=[], body=[ast.Pass(), ast.Pass()])}
        injected_file_map = inject_corelib_sys_path_shim(linker_file_map)

        expected_python = cleandoc(
            """
            import sys
            import pathlib
            lib_path = pathlib.Path(__file__).absolute().parent
            if lib_path not in sys.path:
                sys.path.append(str(lib_path))
            pass
            pass
        """
        )

        assert ast.unparse(injected_file_map["__init__.py"]) == expected_python

    def test_inject_corelib_sys_path_shim_default(self) -> None:
        linker_file_map = {"__init__.py": ast.Module(type_ignores=[], body=[])}
        injected_file_map = inject_corelib_sys_path_shim(linker_file_map)

        expected_python = cleandoc(
            """
            import sys
            import pathlib
            lib_path = pathlib.Path(__file__).absolute().parent
            if lib_path not in sys.path:
                sys.path.append(str(lib_path))
        """
        )

        assert ast.unparse(injected_file_map["__init__.py"]) == expected_python
