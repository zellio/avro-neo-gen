import ast
from inspect import cleandoc

from avro.schema import RecordSchema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema_record_builder import (
    _compile_build_func,
    _compile_field_func,
    compile_avro_schema_record_builder,
)


class TestCompilerCompileAvroSchemaRecord:
    def test__compile_field_func(self, avro_record_schema: RecordSchema) -> None:
        expected_python = cleandoc(
            """
            def favorite_color(self, value: Optional[str]) -> 'UserBuilder':
                self._state['favorite_color'] = value
                return self
        """
        )

        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)

        field = avro_schema.fields[2]
        assert (
            ast.unparse(
                ast.Module(
                    type_ignores=[],
                    body=[
                        _compile_field_func(
                            builder_type_signature=ast.Constant(value="UserBuilder"),
                            avro_schema=field,
                        )
                    ],
                )
            )
            == expected_python
        )

    def test__compile_build_func(self, avro_record_schema: RecordSchema) -> None:
        expected_python = cleandoc(
            """
            def build(self) -> 'User':
                return User(**self._state)
        """
        )

        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)
        assert (
            ast.unparse(
                ast.Module(
                    type_ignores=[],
                    body=[_compile_build_func(avro_schema=avro_schema)],
                )
            )
            == expected_python
        )

    def test_compile_avro_schema_record_builder(self, avro_record_schema: RecordSchema) -> None:

        expected_python = cleandoc(
            """
            class UserBuilder(AbstractNeoGenRecordBuilder):

                def name(self, value: str) -> 'UserBuilder':
                    self._state['name'] = value
                    return self

                def favorite_number(self, value: Optional[int]) -> 'UserBuilder':
                    self._state['favorite_number'] = value
                    return self

                def favorite_color(self, value: Optional[str]) -> 'UserBuilder':
                    self._state['favorite_color'] = value
                    return self

                def build(self) -> 'User':
                    return User(**self._state)
        """
        )

        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)
        assert (
            ast.unparse(
                ast.Module(
                    type_ignores=[],
                    body=[compile_avro_schema_record_builder(avro_schema=avro_schema)],
                )
            )
            == expected_python
        )

        pass
