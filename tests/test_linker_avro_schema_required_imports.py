import json
from typing import Callable, Iterable, Optional, Union

import avro.schema
import pytest
from avro.schema import (
    EnumSchema,
    FixedDecimalSchema,
    FixedSchema,
    LogicalSchema,
    PrimitiveSchema,
)

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_parser_namespace_map import (
    compile_parser_namespace_map,
)
from avro_neo_gen.linker.avro_schema_required_imports import (
    avro_schema_required_imports,
)
from avro_neo_gen.parser.parse_schema import parse_schema
from avro_neo_gen.type_defs import CompilerNamespaceMapCell, LinkerRequiredImports
from avro_neo_gen.utils import dict_func_reduce, flat_map


class TestLinkerAvroSchemaRequiredImports:
    def test_avro_schema_required_imports(
        self,
        avro_primitive_schema_factory: Callable[[str, Optional[str]], PrimitiveSchema],
        avro_enum_schema: EnumSchema,
        avro_fixed_decimal_schema: FixedDecimalSchema,
        avro_fixed_schema: FixedSchema,
        avro_record_schema_json: str,
    ) -> None:
        schema = json.loads(avro_record_schema_json)
        schemas = (
            avro.schema.parse(
                json.dumps(
                    schema
                    | {
                        "name": "ComTest",
                        "namespace": "com.acme",
                        "fields": [{"name": "org_test", "type": schema | {"name": "OrgTest", "namespace": "org.acme"}}],
                    }
                )
            ),
            avro_enum_schema,
            avro_fixed_decimal_schema,
            avro_fixed_schema,
            avro.schema.parse(json.dumps({"type": "bytes", "logical_type": "decimal", "precision": 3})),
            avro_primitive_schema_factory("string", "uuid"),
            avro_primitive_schema_factory("int", "date"),
            avro_primitive_schema_factory("int", "time-millis"),
            avro_primitive_schema_factory("long", "timestamp-millis"),
            avro.schema.parse(json.dumps(["double", "null"])),
            avro.schema.parse(json.dumps(["string", "long", "null"])),
            avro.schema.parse(json.dumps(["string", "long", "null"])),
        )
        parser_namespace_map = parse_schema(schemas)
        compiler_namespace_map = compile_parser_namespace_map(parser_namespace_map)

        def _mapper(cells: Iterable[CompilerNamespaceMapCell]) -> list[AvroSchema]:
            return [cell["schema"] for cell in cells]

        linker_required_imports: list[LinkerRequiredImports] = [
            avro_schema_required_imports(schema) for schema in flat_map(_mapper, compiler_namespace_map.values())
        ]

        assert dict_func_reduce(set.union, linker_required_imports) == {
            "avro_neo_gen.core": {
                "AbstractNeoGenRecordBuilder",
                "NeoGenEnum",
                "NeoGenFixed",
                "NeoGenFixedDecimal",
                "NeoGenRecord",
            },
            "avro_neo_gen.core.utils": {"record_builder_internal"},
            "collections": {"OrderedDict"},
            "datetime": {"date", "datetime", "time"},
            "org.acme": {"OrgTest"},
            "typing": {"Union", "Optional"},
            "uuid": {"UUID"},
        }

    def test_avro_schema_required_imports_unhappy(
        self,
        avro_primitive_schema_factory: Callable[[str, Optional[str]], Union[LogicalSchema, PrimitiveSchema]],
    ) -> None:
        invalid_avro_schema: AvroSchema[PrimitiveSchema] = AvroSchema(avro_primitive_schema_factory("string", None))
        invalid_avro_schema._schema = None
        with pytest.raises(NotImplementedError):
            _ = avro_schema_required_imports(invalid_avro_schema)

        invalid_logical_schema: AvroSchema[LogicalSchema] = AvroSchema(avro_primitive_schema_factory("string", "uuid"))
        invalid_logical_schema._schema.logical_type = "baz"
        with pytest.raises(NotImplementedError):
            _ = avro_schema_required_imports(invalid_logical_schema)
