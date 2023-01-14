import ast
import json
from inspect import cleandoc

import avro.schema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_parser_namespace_map import (
    compile_parser_namespace_map,
)
from avro_neo_gen.linker.link_compiler_namespace_map import link_compiler_namespace_map
from avro_neo_gen.parser.parse_schema import parse_schema


class TestLinkerLinkCompilerNamespaceMap:
    def test_link_compiler_namespace_map(self, avro_record_schema_json: str) -> None:
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
        linker_file_map = link_compiler_namespace_map(compiler_namespace_map)

        assert set(linker_file_map.keys()) == {"com/acme/__init__.py", "org/acme/__init__.py"}

        expected_org_python = cleandoc(
            """
            from avro_neo_gen.core import AbstractNeoGenRecordBuilder, NeoGenRecord
            from avro_neo_gen.core.utils import record_builder_internal
            from collections import OrderedDict
            from typing import Optional

            class OrgTest(NeoGenRecord):
                __canonical_schema__ = OrderedDict(name='org.acme.OrgTest', type='record', fields=[OrderedDict([('name', 'name'), ('type', 'string')]), OrderedDict([('name', 'favorite_number'), ('type', ['int', 'null'])]), OrderedDict([('name', 'favorite_color'), ('type', ['string', 'null'])])])
                __schema__ = dict(type='record', name='OrgTest', namespace='org.acme', fields=[{'type': 'string', 'name': 'name'}, {'type': ['int', 'null'], 'name': 'favorite_number'}, {'type': ['string', 'null'], 'name': 'favorite_color'}])

                def __init__(self, name: str, favorite_number: Optional[int], favorite_color: Optional[str]) -> None:
                    self._datum = record_builder_internal(self_name='self')

                @property
                def name(self) -> str:
                    return self._datum['name']

                @name.setter
                def name(self, value: str) -> None:
                    self._datum['name'] = value

                @property
                def favorite_number(self) -> Optional[int]:
                    return self._datum['favorite_number']

                @favorite_number.setter
                def favorite_number(self, value: Optional[int]) -> None:
                    self._datum['favorite_number'] = value

                @property
                def favorite_color(self) -> Optional[str]:
                    return self._datum['favorite_color']

                @favorite_color.setter
                def favorite_color(self, value: Optional[str]) -> None:
                    self._datum['favorite_color'] = value

            class OrgTestBuilder(AbstractNeoGenRecordBuilder):

                def name(self, value: str) -> 'OrgTestBuilder':
                    self._state['name'] = value
                    return self

                def favorite_number(self, value: Optional[int]) -> 'OrgTestBuilder':
                    self._state['favorite_number'] = value
                    return self

                def favorite_color(self, value: Optional[str]) -> 'OrgTestBuilder':
                    self._state['favorite_color'] = value
                    return self

                def build(self) -> 'OrgTest':
                    return OrgTest(**self._state)
        """
        )
        assert ast.unparse(linker_file_map["org/acme/__init__.py"]) == expected_org_python

        expected_com_python = cleandoc(
            """
            from avro_neo_gen.core import AbstractNeoGenRecordBuilder, NeoGenRecord
            from avro_neo_gen.core.utils import record_builder_internal
            from collections import OrderedDict
            from org.acme import OrgTest

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
        assert ast.unparse(linker_file_map["com/acme/__init__.py"]) == expected_com_python
