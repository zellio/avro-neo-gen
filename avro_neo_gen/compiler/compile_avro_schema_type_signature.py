"""Compile a python AST for the type signature of a given Avro schema."""

import contextlib
from ast import AST, Constant, Load, Name, Subscript, Tuple
from typing import Union

from avro.schema import (
    ArraySchema,
    Field,
    LogicalSchema,
    MapSchema,
    NamedSchema,
    PrimitiveSchema,
    Schema,
    UnionSchema,
)

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.utils import pyast_load_name


def _logical_schema_type_signature(avro_schema: AvroSchema[LogicalSchema]) -> Name:
    match avro_schema.logical_type:  # noqa: R503 - Base case raises exception
        case "uuid":
            return pyast_load_name("UUID")
        case "date":
            return pyast_load_name("date")
        case "time-millis" | "time-micros":
            return pyast_load_name("time")
        case "timestamp-millis" | "timestamp-micros":
            return pyast_load_name("datetime")
        case _:
            raise NotImplementedError


def _primitve_schmea_type_signautre(
    avro_schema: AvroSchema[Union[PrimitiveSchema, LogicalSchema]]
) -> Union[Constant, Name]:
    """Generate a type signature Python AST.

    :param avro_schema: An Avro Primitive Schema.
    :type AvroSchema: :class:`avro.schema.PrimitiveSchema`
    :returns: Python AST of the primitive type signature, usually just the
        name of the type.
    :rtype: :class:`ast.AST`

    Type signatures are fairly obvious, with most of them being either direct
    translations or shortening of the Avro Types.

    Per the spec the mapping is:
      null     = None
      boolean  = bool
      int      = int
      long     = int
      float    = float
      double   = float
      bytes    = bytearray
      string   = str

    """
    if isinstance(avro_schema.schema, LogicalSchema):
        with contextlib.suppress(NotImplementedError):
            return _logical_schema_type_signature(avro_schema)

    match avro_schema.type:  # noqa: R503 - Base case raises exception
        case "null":
            return Constant(value=None)
        case "boolean":
            return pyast_load_name("bool")
        case "int" | "long":
            return pyast_load_name("int")
        case "float" | "double":
            return pyast_load_name("float")
        case "bytes":
            return pyast_load_name("bytearray")
        case "string":
            return pyast_load_name("str")
        case _:
            raise NotImplementedError


def _array_schema_type_signautre(avro_schema: AvroSchema) -> AST:
    """Generate a type signature Python AST.

    Type signature is: list[ items' type ]

    :param avro_schema: An Avro Array Schema.
    :type AvroSchema: avro.schema.ArraySchema
    :returns: AST
    :rtype: ast.AST
    """
    return Subscript(
        value=pyast_load_name("list"),
        slice=compile_avro_schema_type_signature(avro_schema.items),
        ctx=Load(),
    )


def _map_schema_type_signautre(avro_schema: AvroSchema) -> AST:
    """Generate a type signature Python AST.

    Type signature is: dict[str, values' type ]

    :param avro_schema: An Avro Map Schema.
    :type AvroSchema: avro.schema.MapSchema
    :returns: AST
    :rtype: ast.AST
    """
    return Subscript(
        value=pyast_load_name("dict"),
        slice=Tuple(
            elts=[
                pyast_load_name("str"),
                compile_avro_schema_type_signature(avro_schema.values),
            ],
            ctx=Load(),
        ),
        ctx=Load(),
    )


def _union_schema_type_signautre(avro_schema: AvroSchema) -> AST:
    """Generate type signature for an Avro Union Schema.

    Method will generate either an Optional or a Union.

    :param avro_schema: Avro Schema of a Union type.
    :type avro_schema: UnionSchema
    :returns: AST
    :rtype: ast.AST
    """
    schemas = sorted(avro_schema.schemas, key=lambda schema: schema.type)
    optional_schemas = [schema for schema in schemas if schema.type != "null"]

    python_ast: AST
    if len(optional_schemas) == 1:
        return Subscript(
            value=pyast_load_name("Optional"),
            slice=compile_avro_schema_type_signature(optional_schemas[0]),
            ctx=Load(),
        )

    etls = [compile_avro_schema_type_signature(AvroSchema(schema)) for schema in optional_schemas]

    if len(optional_schemas) != len(schemas):
        etls.append(Constant(value=None))

    return Subscript(
        value=pyast_load_name("Union"),
        slice=Tuple(elts=etls, ctx=Load()),
        ctx=Load(),
    )


def _named_schema_type_signautre(avro_schema: AvroSchema) -> AST:
    """Generate a name reference to the generated class.

    :param avro_schema: An Avro Named Schema.
    :type AvroSchema: avro.schema.NamedSchema
    :returns: AST
    :rtype: ast.Name
    """
    avro_schema = AvroSchema(schema=avro_schema)
    return Constant(value=avro_schema.name)


def compile_avro_schema_type_signature(avro_schema: AvroSchema[Schema]) -> AST:
    """Generate a Python type signature from an Avro Schema or Protocol.

    :param avro_schema: Avro type to be compiled.
    :type avro_schema: :class:`AvroSchema`[:class:`avro.schema.Schema`]
    :returns: Python AST type signature
    :rtype: :class:`ast.AST`
    """
    match avro_schema.schema:  # noqa: R503 - Base case raises exception
        case PrimitiveSchema():  # type: ignore
            return _primitve_schmea_type_signautre(avro_schema)
        case ArraySchema():  # type: ignore
            return _array_schema_type_signautre(avro_schema)
        case MapSchema():  # type: ignore
            return _map_schema_type_signautre(avro_schema)
        case UnionSchema():  # type: ignore
            return _union_schema_type_signautre(avro_schema)
        case Field():  # type: ignore
            return compile_avro_schema_type_signature(AvroSchema(avro_schema.type))
        case NamedSchema():  # type: ignore
            return _named_schema_type_signautre(avro_schema)
        case _:
            raise NotImplementedError
