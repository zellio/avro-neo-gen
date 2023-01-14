"""Impl."""

import importlib
import sys
from json import dumps as json_encode
from json import loads as json_decode
from types import ModuleType
from typing import Callable, Generator, Optional, Union

from avro.schema import (
    EnumSchema,
    FixedDecimalSchema,
    FixedSchema,
    LogicalSchema,
    NamedSchema,
    PrimitiveSchema,
    RecordSchema,
)
from avro.schema import parse as avro_schema_parse
from pyfakefs.fake_filesystem import FakeFilesystem, PatchMode
from pytest import fixture

from avro_neo_gen.core.driver.driver_proxy import DriverProxy


@fixture
def fake_filesystem(fs: FakeFilesystem) -> Generator[FakeFilesystem, None, None]:
    """Provide a longer name for auto-installed ``fs`` fixture."""
    yield fs


@fixture
def avro_primitive_schema_json_factory() -> Generator[Callable[[str, Optional[str]], str], None, None]:
    def _avro_primitive_schema_factory(type_name: str, logical_type_name: Optional[str] = None) -> str:
        json_schema = {"type": type_name}
        if logical_type_name:
            json_schema["logicalType"] = logical_type_name
        return json_encode(json_schema)

    yield _avro_primitive_schema_factory


@fixture
def avro_primitive_schema_factory(
    avro_primitive_schema_json_factory: Callable[[str, Optional[str]], str]
) -> Generator[Callable[[str, Optional[str]], Union[PrimitiveSchema, LogicalSchema]], None, None]:  # noqa: Fn type sig
    def _avro_primitive_schema_factory(
        type_name: str, logical_type_name: Optional[str] = None
    ) -> Union[PrimitiveSchema, LogicalSchema]:
        json_schmea = avro_primitive_schema_json_factory(type_name, logical_type_name)
        return avro_schema_parse(json_schmea)

    yield _avro_primitive_schema_factory


@fixture
def avro_record_schema_json() -> Generator[str, None, None]:
    yield json_encode(
        {
            "namespace": "com.acme",
            "type": "record",
            "name": "User",
            "fields": [
                {"name": "name", "type": "string"},
                {"name": "favorite_number", "type": ["int", "null"]},
                {"name": "favorite_color", "type": ["string", "null"]},
            ],
        }
    )


@fixture
def avro_record_schema(avro_record_schema_json: str) -> Generator[RecordSchema, None, None]:
    yield avro_schema_parse(avro_record_schema_json)


@fixture
def avro_enum_schema_json() -> Generator[str, None, None]:
    yield json_encode({"type": "enum", "name": "Suit", "symbols": ["SPADES", "HEARTS", "DIAMONDS", "CLUBS"]})


@fixture
def avro_enum_schema(avro_enum_schema_json: str) -> Generator[EnumSchema, None, None]:
    yield avro_schema_parse(avro_enum_schema_json)


@fixture
def avro_fixed_schema_json() -> Generator[str, None, None]:
    yield json_encode(
        {
            "type": "fixed",
            "size": 16,
            "name": "MD5",
        }
    )


@fixture
def avro_fixed_schema(avro_fixed_schema_json: str) -> Generator[FixedSchema, None, None]:
    yield avro_schema_parse(avro_fixed_schema_json)


@fixture
def avro_fixed_decimal_schema_json() -> Generator[str, None, None]:
    yield json_encode(
        {"type": "fixed", "logicalType": "decimal", "size": 16, "name": "FixNum", "precision": 4, "scale": 2}
    )


@fixture
def avro_fixed_decimal_schema(
    avro_fixed_decimal_schema_json: FixedDecimalSchema,
) -> Generator[FixedDecimalSchema, None, None]:
    yield avro_schema_parse(avro_fixed_decimal_schema_json)


def _compile_schema(fake_filesystem: FakeFilesystem, schema: NamedSchema) -> ModuleType:
    from avro_neo_gen.avro_schema import AvroSchema
    from avro_neo_gen.compiler.compile_parser_namespace_map import (
        compile_parser_namespace_map,
    )
    from avro_neo_gen.linker.emit_linker_file_map import emit_linker_file_map
    from avro_neo_gen.linker.link_compiler_namespace_map import (
        link_compiler_namespace_map,
    )
    from avro_neo_gen.parser.parse_schema import parse_schema

    avro_schema: AvroSchema[NamedSchema] = AvroSchema(
        avro_schema_parse(json_encode(json_decode(schema) | {"namespace": ""}))
    )
    parser_namespace_map = parse_schema([avro_schema])
    compiler_namespace_map = compile_parser_namespace_map(parser_namespace_map)
    linker_file_map = link_compiler_namespace_map(compiler_namespace_map)
    fake_filesystem.patch_open_code = PatchMode.AUTO
    fake_filesystem.create_file("/generated/__init__.py", create_missing_dirs=True, encoding="utf-8")
    emit_linker_file_map(linker_file_map, "/generated")
    spec = importlib.util.spec_from_file_location("generated", "/generated/__init__.py")
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules["generated"] = module
    spec.loader.exec_module(module)  # type: ignore
    return module


@fixture
def neo_gen_record_module(
    fake_filesystem: FakeFilesystem, avro_record_schema_json: str
) -> Generator[ModuleType, None, None]:
    yield _compile_schema(fake_filesystem, avro_record_schema_json)


@fixture
def neo_gen_enum_module(
    fake_filesystem: FakeFilesystem, avro_enum_schema_json: str
) -> Generator[ModuleType, None, None]:
    yield _compile_schema(fake_filesystem, avro_enum_schema_json)


@fixture
def neo_gen_fixed_module(
    fake_filesystem: FakeFilesystem, avro_fixed_schema_json: str
) -> Generator[ModuleType, None, None]:
    yield _compile_schema(fake_filesystem, avro_fixed_schema_json)


@fixture
def neo_gen_fixed_decimal_module(
    fake_filesystem: FakeFilesystem, avro_fixed_decimal_schema_json: str
) -> Generator[ModuleType, None, None]:
    yield _compile_schema(fake_filesystem, avro_fixed_decimal_schema_json)


@fixture
def stateless_driver_proxy_factory() -> Generator[Callable[[str], DriverProxy], None, None]:
    driver_proxy = DriverProxy()

    def _stateless_driver_proxy_factory(module: str) -> DriverProxy:
        DriverProxy.load_driver(module)
        return driver_proxy

    yield _stateless_driver_proxy_factory

    driver_proxy._driver_module = None
    driver_proxy._driver_class = None
    driver_proxy._driver = None


@fixture
def apache_avro_binary_core_driver_proxy(
    stateless_driver_proxy_factory: Callable[[str], DriverProxy]
) -> Generator["DriverProxy", None, None]:
    yield stateless_driver_proxy_factory("avro_neo_gen.core.driver.apache_avro_binary_driver")
