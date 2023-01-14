from ast import Module, Pass
from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem

from avro_neo_gen.linker.emit_linker_file_map import emit_linker_file_map


class TestLinkerEmitLinkerFileMap:
    def test_emit_linker_file_map(self, fake_filesystem: FakeFilesystem) -> None:
        fake_filesystem.create_dir("target")
        emit_linker_file_map(
            linker_file_map={"foo/bar/test.py": Module(body=[Pass(), Pass(), Pass()], type_ignores=[])},
            base_path="target",
        )

        generated_path = Path("target/foo/bar/test.py")

        assert generated_path.exists()
        assert generated_path.read_text(encoding="utf-8") == "pass\npass\npass\n"
