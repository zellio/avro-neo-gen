import ast
import json
from typing import Callable, Optional

import avro.schema
import pytest
from avro.schema import (
    ArraySchema,
    EnumSchema,
    Field,
    LogicalSchema,
    MapSchema,
    PrimitiveSchema,
    RecordSchema,
    Schema,
    UnionSchema,
)

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema_type_signature import (
    compile_avro_schema_type_signature,
)


class TestCompilerCompileAvroSchemaTypeSignature:
    def test_compile_pyast_type_signaure(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[Schema] = AvroSchema(avro_record_schema)
        avro_schema._schema = ["weird-type"]

        with pytest.raises(NotImplementedError):
            compile_avro_schema_type_signature(avro_schema)

    def test_compile_pyast_type_signaure_primitive_types(
        self,
        avro_primitive_schema_factory: Callable[[str, Optional[str]], PrimitiveSchema],
    ) -> None:
        primitive_type_map = {
            ("null",): "None",
            ("boolean",): "bool",
            ("int",): "int",
            ("long",): "int",
            ("float",): "float",
            ("double",): "float",
            ("bytes",): "bytearray",
            ("string",): "str",
            ("string", "uuid"): "UUID",
            ("int", "date"): "date",
            ("int", "time-millis"): "time",
            ("long", "time-micros"): "time",
            ("long", "timestamp-millis"): "datetime",
            ("long", "timestamp-micros"): "datetime",
        }

        for avro_type, expected_python in primitive_type_map.items():
            avro_schema: AvroSchema[PrimitiveSchema] = AvroSchema(avro_primitive_schema_factory(*avro_type))
            assert ast.unparse(compile_avro_schema_type_signature(avro_schema)) == expected_python

        fake_avro_primitive = avro_primitive_schema_factory("int", "date")
        fake_avro_primitive.logical_type = "foo"
        fake_avro_schema: AvroSchema[LogicalSchema] = AvroSchema(fake_avro_primitive)
        assert ast.unparse(compile_avro_schema_type_signature(fake_avro_schema)) == "int"

        fake_avro_primitive.type = "bang"
        avro_schema_logical: AvroSchema[LogicalSchema] = AvroSchema(fake_avro_primitive)
        with pytest.raises(NotImplementedError):
            _ = compile_avro_schema_type_signature(avro_schema_logical)

    def test_compile_pyast_type_signaure_array(self) -> None:
        json_schema = {"type": "array", "items": "int"}
        avro_schema: AvroSchema[ArraySchema] = AvroSchema(avro.schema.parse(json.dumps(json_schema)))
        expected_python = "list[int]"
        assert ast.unparse(compile_avro_schema_type_signature(avro_schema)) == expected_python

    def test_compile_pyast_type_signaure_map(self) -> None:
        json_schema = {"type": "map", "values": "int"}
        avro_schema: AvroSchema[MapSchema] = AvroSchema(avro.schema.parse(json.dumps(json_schema)))
        expected_python = "dict[str, int]"
        assert ast.unparse(compile_avro_schema_type_signature(avro_schema)) == expected_python

    def test_compile_avro_schema_type_signature_union(self) -> None:
        json_schema = ["long", "double"]
        avro_schema: AvroSchema[UnionSchema] = AvroSchema(avro.schema.parse(json.dumps(json_schema)))
        expected_python = "Union[float, int]"
        assert ast.unparse(compile_avro_schema_type_signature(avro_schema)) == expected_python

    def test_compile_avro_schema_type_signature_union_optional(self) -> None:
        json_schema = ["long", "null"]
        avro_schema: AvroSchema[UnionSchema] = AvroSchema(avro.schema.parse(json.dumps(json_schema)))
        expected_python = "Optional[int]"
        assert ast.unparse(compile_avro_schema_type_signature(avro_schema)) == expected_python

    def test_compile_avro_schema_type_signature_union_optional_union(self) -> None:
        json_schema = ["string", "boolean", "null"]
        avro_schema: AvroSchema[UnionSchema] = AvroSchema(avro.schema.parse(json.dumps(json_schema)))
        expected_python = "Union[bool, str, None]"
        assert ast.unparse(compile_avro_schema_type_signature(avro_schema)) == expected_python

    def test_compile_avro_schema_type_signature_field(self, avro_record_schema: RecordSchema) -> None:
        field: AvroSchema[Field] = AvroSchema(avro_record_schema.fields[0])
        assert ast.unparse(compile_avro_schema_type_signature(field)) == ast.unparse(
            compile_avro_schema_type_signature(field.type)
        )

    def test_compile_avro_schema_type_signature_named_schema(
        self, avro_record_schema: RecordSchema, avro_enum_schema: EnumSchema
    ) -> None:
        expected_python = "'User'"
        assert ast.unparse(compile_avro_schema_type_signature(AvroSchema(avro_record_schema))) == expected_python

        expected_python = "'Suit'"
        assert ast.unparse(compile_avro_schema_type_signature(AvroSchema(avro_enum_schema))) == expected_python
