import ast
from inspect import cleandoc

from avro.schema import RecordSchema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema_record_body import (
    _compile_field_property_funcs,
    _compile_init_func,
    compile_avro_schema_record_body,
)


class TestCompilerCompileAvroSchemaRecord:
    def test__compile_init_func(self, avro_record_schema: RecordSchema) -> None:
        expected_python = cleandoc(
            """
            def __init__(self, name: str, favorite_number: Optional[int], favorite_color: Optional[str]) -> None:
                self._datum = record_builder_internal(self_name='self')
        """
        )

        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)
        assert ast.unparse(_compile_init_func(avro_schema)) == expected_python

    def test__compile_field_property_funcs(self, avro_record_schema: RecordSchema) -> None:
        expected_python = cleandoc(
            """
            @property
            def favorite_color(self) -> Optional[str]:
                return self._datum['favorite_color']

            @favorite_color.setter
            def favorite_color(self, value: Optional[str]) -> None:
                self._datum['favorite_color'] = value
        """
        )

        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)
        assert (
            ast.unparse(ast.Module(type_ignores=[], body=_compile_field_property_funcs(avro_schema.fields[2])))
            == expected_python
        )

    def test_compile_avro_schema_record_body(self, avro_record_schema: RecordSchema) -> None:
        expected_python = cleandoc(
            """
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
        """
        )

        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)
        assert (
            ast.unparse(ast.Module(type_ignores=[], body=compile_avro_schema_record_body(avro_schema)))
            == expected_python
        )
