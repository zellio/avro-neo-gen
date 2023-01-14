import json

import avro.schema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_parser_namespace_map import (
    compile_parser_namespace_map,
)
from avro_neo_gen.linker.link_module import link_module
from avro_neo_gen.parser.parse_schema import parse_schema


class TestLinkerLinkModule:
    def test_link_module_base(self) -> None:
        module_file_map = link_module({})
        assert set(module_file_map.keys()) == {
            "__init__.py",
            "avro_neo_gen/core/__init__.py",
            "avro_neo_gen/core/abstract_neo_gen_object.py",
            "avro_neo_gen/core/abstract_neo_gen_record_builder.py",
            "avro_neo_gen/core/driver/__init__.py",
            "avro_neo_gen/core/driver/abstract_avro_driver.py",
            "avro_neo_gen/core/driver/apache_avro_binary_driver.py",
            "avro_neo_gen/core/driver/avro_driver_type.py",
            "avro_neo_gen/core/driver/driver_proxy.py",
            "avro_neo_gen/core/neo_gen_builder.py",
            "avro_neo_gen/core/neo_gen_encodable.py",
            "avro_neo_gen/core/neo_gen_enum.py",
            "avro_neo_gen/core/neo_gen_error.py",
            "avro_neo_gen/core/neo_gen_fixed.py",
            "avro_neo_gen/core/neo_gen_record.py",
            "avro_neo_gen/core/neo_gen_type.py",
            "avro_neo_gen/core/type_defs.py",
            "avro_neo_gen/core/utils.py",
        }

    def test_link_module(self, avro_record_schema_json: str) -> None:
        schema = json.loads(avro_record_schema_json)
        com_record = avro.schema.parse(
            json.dumps(
                schema
                | {
                    "name": "ComTest",
                    "namespace": "com.acme",
                    "fields": [{"name": "org_test", "type": schema | {"name": "OrgTest", "namespace": "org.acme"}}],
                }
            )
        )

        parser_namespace_map = parse_schema([AvroSchema(com_record)])
        compiler_namespace_map = compile_parser_namespace_map(parser_namespace_map)

        module_file_map = link_module(compiler_namespace_map)
        assert set(module_file_map.keys()) == {
            "__init__.py",
            "com/acme/__init__.py",
            "org/acme/__init__.py",
            "avro_neo_gen/core/__init__.py",
            "avro_neo_gen/core/abstract_neo_gen_object.py",
            "avro_neo_gen/core/abstract_neo_gen_record_builder.py",
            "avro_neo_gen/core/driver/__init__.py",
            "avro_neo_gen/core/driver/abstract_avro_driver.py",
            "avro_neo_gen/core/driver/apache_avro_binary_driver.py",
            "avro_neo_gen/core/driver/avro_driver_type.py",
            "avro_neo_gen/core/driver/driver_proxy.py",
            "avro_neo_gen/core/neo_gen_builder.py",
            "avro_neo_gen/core/neo_gen_encodable.py",
            "avro_neo_gen/core/neo_gen_enum.py",
            "avro_neo_gen/core/neo_gen_error.py",
            "avro_neo_gen/core/neo_gen_fixed.py",
            "avro_neo_gen/core/neo_gen_record.py",
            "avro_neo_gen/core/neo_gen_type.py",
            "avro_neo_gen/core/type_defs.py",
            "avro_neo_gen/core/utils.py",
        }
