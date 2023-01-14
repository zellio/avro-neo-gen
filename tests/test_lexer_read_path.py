from pathlib import Path

import avro.schema
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from avro_neo_gen.lexer import read_path


class TestLexerReadPath:
    def test_read_path_happy(
        self,
        fake_filesystem: FakeFilesystem,
        avro_record_schema_json: str,
        avro_record_schema: avro.schema.Schema,
    ) -> None:
        fake_filesystem.create_file(file_path="source/record.avsc", create_missing_dirs=True, encoding="utf-8")
        Path("source/record.avsc").write_text(data=avro_record_schema_json, encoding="utf-8")

        schemas = read_path("source/record.avsc")
        read_schema = next(schemas)
        assert read_schema is not avro_record_schema
        assert read_schema == avro_record_schema

        schemas = read_path(Path("source"))
        read_schema = next(schemas)
        assert read_schema is not avro_record_schema
        assert read_schema == avro_record_schema

    def test_read_path_unhappy(
        self,
        fake_filesystem: FakeFilesystem,
    ) -> None:
        fake_filesystem.create_dir("source")

        Path("source/list.avsc").write_text(data="[]", encoding="utf-8")
        with pytest.raises(NotImplementedError):
            _ = next(read_path(Path("source")))

        Path("source/list.avsc").write_text(data='"string"', encoding="utf-8")
        with pytest.raises(NotImplementedError):
            _ = next(read_path(Path("source")))

        Path("source/list.avsc").write_text(data="null", encoding="utf-8")
        with pytest.raises(NotImplementedError):
            _ = next(read_path(Path("source")))
