import ast
from inspect import cleandoc

import pytest
from avro.schema import EnumSchema, FixedDecimalSchema, FixedSchema, RecordSchema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema import compile_avro_schema
from avro_neo_gen.utils import pyast_module


class TestCompilerCompilePyast:
    def test_compile_avro_schema(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[RecordSchema] = AvroSchema(avro_record_schema)
        avro_schema._schema = ["weird-type"]

        with pytest.raises(NotImplementedError):
            compile_avro_schema(avro_schema)

    def test_compile_avro_schema_enum(self, avro_enum_schema: EnumSchema) -> None:
        expected_python = cleandoc(
            """
            class Suit(NeoGenEnum):
                __canonical_schema__ = OrderedDict(name='Suit', type='enum', symbols=['SPADES', 'HEARTS', 'DIAMONDS', 'CLUBS'])
                __schema__ = dict(type='enum', name='Suit', symbols=['SPADES', 'HEARTS', 'DIAMONDS', 'CLUBS'])
        """
        )

        compiled_python = ast.unparse(pyast_module(body=compile_avro_schema(AvroSchema(avro_enum_schema))))

        assert expected_python == compiled_python

    def test_compile_avro_schema_fixed_schema(self, avro_fixed_schema: FixedSchema) -> None:
        expected_python = cleandoc(
            """
            class MD5(NeoGenFixed):
                __canonical_schema__ = OrderedDict(name='MD5', type='fixed', size=16)
                __schema__ = dict(type='fixed', name='MD5', size=16)
        """
        )

        compiled_python = ast.unparse(pyast_module(body=compile_avro_schema(AvroSchema(avro_fixed_schema))))

        assert expected_python == compiled_python

    def test_compile_avro_schema_fixed_decimal_schema(self, avro_fixed_decimal_schema: FixedDecimalSchema) -> None:
        expected_python = cleandoc(
            """
            class FixNum(NeoGenFixedDecimal):
                __canonical_schema__ = OrderedDict(name='FixNum', type='fixed', size=16)
                __schema__ = dict(type='fixed', logicalType='decimal', precision=4, scale=2, name='FixNum', size=16)
        """
        )

        compiled_python = ast.unparse(pyast_module(body=compile_avro_schema(AvroSchema(avro_fixed_decimal_schema))))

        assert expected_python == compiled_python
