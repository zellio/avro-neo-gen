"""Compile *Builder Class for a given Avro Schema."""

from ast import (
    Assign,
    Attribute,
    Call,
    ClassDef,
    Constant,
    FunctionDef,
    Load,
    Return,
    Store,
    Subscript,
    arg,
    arguments,
    keyword,
)

from avro.schema import Field, RecordSchema

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema_type_signature import (
    compile_avro_schema_type_signature,
)
from avro_neo_gen.utils import pyast_load_name


def _compile_field_func(avro_schema: AvroSchema[Field], builder_type_signature: Constant) -> FunctionDef:
    field_name = avro_schema.schema.name
    self_load_name = pyast_load_name("self")
    return FunctionDef(
        lineno=None,
        decorator_list=[],
        name=field_name,
        args=arguments(
            posonlyargs=[],
            args=[arg(arg="self"), arg(arg="value", annotation=compile_avro_schema_type_signature(avro_schema))],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            Assign(
                lineno=None,
                targets=[
                    Subscript(
                        value=Attribute(value=self_load_name, attr="_state", ctx=Load()),
                        slice=Constant(field_name),
                        ctx=Store(),
                    )
                ],
                value=pyast_load_name("value"),
            ),
            Return(value=self_load_name),
        ],
        returns=builder_type_signature,
    )


def _compile_build_func(avro_schema: AvroSchema[RecordSchema]) -> FunctionDef:
    return FunctionDef(
        lineno=None,
        decorator_list=[],
        name="build",
        args=arguments(
            posonlyargs=[],
            args=[arg(arg="self")],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        returns=compile_avro_schema_type_signature(avro_schema),
        body=[
            Return(
                value=Call(
                    func=pyast_load_name(avro_schema.schema.name),
                    args=[],
                    keywords=[keyword(value=Attribute(value=pyast_load_name("self"), attr="_state", ctx=Load()))],
                )
            )
        ],
    )


def compile_avro_schema_record_builder(avro_schema: AvroSchema[RecordSchema]) -> ClassDef:
    """Generate a Builder class def for a given AvroSchema.

    :param avro_schema: :class:`AvroSchema` containing a RecordSchema to
        generate a builder class for.
    :type avro_schema: :class:`AvroSchema`[:class:`avro.schema.RecordSchema`]
    :return: Python AST representation of the Builder class for a given AvroSchema.
    :rtype: :class:`ast.ClassDef`

    .. note:: Only Record types get builders, everything else is self building.
    """
    builder_name = f"{avro_schema.name}Builder"
    builder_type_signature = Constant(value=builder_name)
    return ClassDef(
        decorator_list=[],
        name=builder_name,
        bases=[pyast_load_name("AbstractNeoGenRecordBuilder")],
        keywords=[],
        body=[
            *[_compile_field_func(field, builder_type_signature) for field in avro_schema.fields],
            _compile_build_func(avro_schema),
        ],
    )
