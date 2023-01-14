"""Compile the AvroSchema record body to pass up to the class compiler."""

from ast import (
    Assign,
    Attribute,
    Call,
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
from avro_neo_gen.utils import flat_map, pyast_load_name


def _compile_init_func(avro_schema: AvroSchema[RecordSchema]) -> FunctionDef:
    return FunctionDef(
        lineno=None,
        decorator_list=[],
        name="__init__",
        args=arguments(
            posonlyargs=[],
            args=[
                arg(arg="self"),
                *[
                    arg(arg=field.schema.name, annotation=compile_avro_schema_type_signature(field))
                    for field in avro_schema.fields
                ],
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        returns=Constant(value=None),
        body=[
            Assign(
                lineno=None,
                targets=[Attribute(value=pyast_load_name("self"), attr="_datum", ctx=Store())],
                value=Call(
                    func=pyast_load_name("record_builder_internal"),
                    args=[],
                    keywords=[keyword(arg="self_name", value=Constant(value="self"))],
                ),
            )
        ],
    )


def _compile_field_property_funcs(avro_schema: AvroSchema[Field]) -> list[FunctionDef]:
    type_signature = compile_avro_schema_type_signature(avro_schema.type)
    # Field.name is forced to be None so we need to directly access the name field of schema.
    field_name = avro_schema.schema.name

    self_arg = arg(arg="self")
    datum_attr_load = Attribute(
        value=pyast_load_name("self"),
        attr="_datum",
        ctx=Load(),
    )
    constant_name = Constant(value=field_name)

    return [
        # Getter func
        FunctionDef(
            lineno=None,
            decorator_list=[pyast_load_name("property")],
            name=field_name,
            args=arguments(posonlyargs=[], args=[self_arg], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=[Return(value=Subscript(value=datum_attr_load, slice=constant_name, ctx=Load()))],
            returns=type_signature,
        ),
        # Setter Func
        FunctionDef(
            lineno=None,
            decorator_list=[
                Attribute(
                    value=pyast_load_name(field_name),
                    attr="setter",
                    ctx=Load(),
                )
            ],
            name=field_name,
            args=arguments(
                posonlyargs=[],
                args=[self_arg, arg(arg="value", annotation=type_signature)],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                Assign(
                    lineno=None,
                    targets=[
                        Subscript(
                            value=datum_attr_load,
                            slice=constant_name,
                            ctx=Store(),
                        )
                    ],
                    value=pyast_load_name("value"),
                )
            ],
            returns=Constant(value=None),
        ),
    ]


def compile_avro_schema_record_body(avro_schema: AvroSchema[RecordSchema]) -> list[FunctionDef]:
    """Compile Record body init and property functions.

    :returns: List of :class:`ast.AST` functions for the internals of a
        :class:`NeoGenRecord`
    :rtype: list[:class:`ast.FunctionDef`]

    """
    return [
        _compile_init_func(avro_schema),
        *flat_map(_compile_field_property_funcs, avro_schema.fields),
    ]
