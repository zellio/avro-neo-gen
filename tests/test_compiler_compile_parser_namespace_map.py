import ast
import json
from inspect import cleandoc

import avro.schema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_parser_namespace_map import (
    compile_parser_namespace_map,
)
from avro_neo_gen.parser.parse_schema import parse_schema
from avro_neo_gen.utils import pyast_module


class TestCompilerCompileParserNamespaceMap:
    def test_compile_parser_namespace_map(self, avro_record_schema_json: str) -> None:
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
        org_record = com_record.fields[0].type

        parser_namespace_map = parse_schema([AvroSchema(com_record)])
        compiler_namespace_map = compile_parser_namespace_map(parser_namespace_map)

        assert "com.acme" in compiler_namespace_map
        assert parser_namespace_map["com.acme"][-1] == com_record
        assert org_record not in parser_namespace_map["com.acme"]

        assert "org.acme" in compiler_namespace_map
        assert parser_namespace_map["org.acme"][-1] == org_record

        expected_python = cleandoc(
            """
            class ComTest(NeoGenRecord):
                __canonical_schema__ = OrderedDict(name='com.acme.ComTest', type='record', fields=[OrderedDict([('name', 'org_test'), ('type', OrderedDict([('name', 'org.acme.OrgTest'), ('type', 'record'), ('fields', [OrderedDict([('name', 'name'), ('type', 'string')]), OrderedDict([('name', 'favorite_number'), ('type', ['int', 'null'])]), OrderedDict([('name', 'favorite_color'), ('type', ['string', 'null'])])])]))])])
                __schema__ = dict(type='record', name='ComTest', namespace='com.acme', fields=[{'type': {'type': 'record', 'name': 'OrgTest', 'namespace': 'org.acme', 'fields': [{'type': 'string', 'name': 'name'}, {'type': ['int', 'null'], 'name': 'favorite_number'}, {'type': ['string', 'null'], 'name': 'favorite_color'}]}, 'name': 'org_test'}])

                def __init__(self, org_test: 'OrgTest') -> None:
                    self._datum = record_builder_internal(self_name='self')

                @property
                def org_test(self) -> 'OrgTest':
                    return self._datum['org_test']

                @org_test.setter
                def org_test(self, value: 'OrgTest') -> None:
                    self._datum['org_test'] = value

            class ComTestBuilder(AbstractNeoGenRecordBuilder):

                def org_test(self, value: 'OrgTest') -> 'ComTestBuilder':
                    self._state['org_test'] = value
                    return self

                def build(self) -> 'ComTest':
                    return ComTest(**self._state)
        """
        )
        assert compiler_namespace_map["com.acme"][-1]["ast"] is not None
        assert ast.unparse(pyast_module(body=compiler_namespace_map["com.acme"][-1]["ast"])) == expected_python
