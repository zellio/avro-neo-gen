"""Compile AvroSchema into Python AST."""

from ast import AST, Assign, Call, ClassDef, Constant, keyword

from avro.schema import (
    EnumSchema,
    FixedDecimalSchema,
    FixedSchema,
    NamedSchema,
    RecordSchema,
)

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.compiler.compile_avro_schema_record_body import (
    compile_avro_schema_record_body,
)
from avro_neo_gen.compiler.compile_avro_schema_record_builder import (
    compile_avro_schema_record_builder,
)
from avro_neo_gen.utils import pyast_load_name


def _named_schema_class_members(avro_schema: AvroSchema[NamedSchema]) -> list[AST]:
    """Generate class schema and canonical_schema fields.

    :param avro_schema: Source Avro schema being compiled.
    :type avro_schema: class:`AvroSchema`
    :return: List of Python AST nodes for field assignment in the class def.
    :rtype: list[:class:`ast.AST`]
    """
    return [
        Assign(
            targets=[pyast_load_name("__canonical_schema__")],
            value=Call(
                func=pyast_load_name("OrderedDict"),
                args=[],
                keywords=[
                    keyword(arg=key, value=Constant(value=value))
                    for key, value in avro_schema.to_canonical_json().items()
                ],
            ),
            lineno=None,
        ),
        Assign(
            targets=[pyast_load_name("__schema__")],
            value=Call(
                func=pyast_load_name("dict"),
                args=[],
                keywords=[
                    keyword(arg=key, value=Constant(value=value)) for key, value in avro_schema.to_json().items()
                ],
            ),
            lineno=None,
        ),
    ]


def _named_schema_class_def(avro_schema: AvroSchema, bases: list[str], body: list[AST]) -> ClassDef:
    """Generate a NeoGenObject subclass AST.

    :param avro_schema: Source Avro schema being compiled.
    :type avro_schema: class:`AvroSchema`
    :param bases: List of the classes to subclass in the generated AST.
    :type bases: list[str]
    :param body: Python AST statements for the body of the generated class.
    :type body: list[:class:`ast.AST`]
    """
    return ClassDef(
        decorator_list=[],
        name=avro_schema.name,
        bases=[pyast_load_name(base) for base in bases],
        keywords=[],
        body=[*_named_schema_class_members(avro_schema), *body],
    )


def compile_avro_schema(avro_schema: AvroSchema[NamedSchema]) -> list[AST]:
    """Compile a named Avro schema into Python AST.

    :param avro_schema: Instance of :class:`AvroSchema` which contains a
        :class:`avro.schema.NamedSchema` to be compiled.
    :type avro_schema: AvroSchema
    :return: The list of Python AST nodes which comprise the bases of the
        compiled source.
    :rtype: list[:class:`ast.AST`]
    """
    match avro_schema.schema:  # noqa: R503 - Base case raises exception
        case RecordSchema():  # type: ignore
            return [
                _named_schema_class_def(
                    avro_schema,
                    ["NeoGenRecord"],
                    compile_avro_schema_record_body(avro_schema),
                ),
                compile_avro_schema_record_builder(avro_schema),
            ]
        case EnumSchema():  # type: ignore
            return [_named_schema_class_def(avro_schema, ["NeoGenEnum"], [])]
        case FixedDecimalSchema():  # type: ignore
            return [_named_schema_class_def(avro_schema, ["NeoGenFixedDecimal"], [])]
        case FixedSchema():  # type: ignore
            return [_named_schema_class_def(avro_schema, ["NeoGenFixed"], [])]
        case _:
            raise NotImplementedError()
