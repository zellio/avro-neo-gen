"""Shared type declarations."""

from typing import Any, Literal, TypedDict, Union

AvroPrimitiveTypeLiteral = Literal[
    "null",
    "boolean",
    "int",
    "long",
    "float",
    "double",
    "bytes",
    "string",
]


class AvroPrimitiveTypeDef(TypedDict, total=False):
    """Primitive schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": str
        }
    """

    type: AvroPrimitiveTypeLiteral  # noqa: VNE003,A003 - Value name based on spec


class AvroRecordFieldTypeDef(TypedDict, total=False):
    """Record field schema type definition per spec 1.11.1.

    ::

        Schema: {
            "name": str,
            "doc": str,
            "type": schema,
            "default": default_value
        }
    """

    name: str
    doc: str  # NotRequired
    type: "AvroSchemaTypeDef"  # noqa: VNE003,A003 - Value name based on spec
    default: Any  # NotRequired


AvroRecordTypeLiteral = Literal["record"]


class AvroRecordTypeDef(TypedDict, total=False):
    """Record schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": "record",
            "name": str,
            "namespace": str,
            "doc": str,
            "aliases": list[str],
            "fields": list[schema]
        }
    """

    type: AvroRecordTypeLiteral  # noqa: VNE003,A003 - Value name based on spec
    name: str
    namespace: str  # NotRequired
    alias: list[str]  # NotRequired
    doc: str  # NotRequired
    fields: list[AvroRecordFieldTypeDef]


AvroEnumTypeLiteral = Literal["enum"]


class AvroEnumTypeDef(TypedDict, total=False):
    """Enum schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": "enum",
            "name": str,
            "namespace": str,
            "doc": str,
            "aliases": list[str],
            "symbols": list[str],
            "default": str
        }
    """

    type: AvroEnumTypeLiteral  # noqa: VNE003,A003 - Value name based on spec
    name: str
    namespace: str  # NotRequired
    alias: list[str]  # NotRequired
    doc: str  # NotRequired
    symbols: list[str]
    default: Any  # NotRequired


AvroArrayTypeLiteral = Literal["array"]


class AvroArrayTypeDef(TypedDict, total=False):
    """Array schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": "array",
            "items": schema,
            "default": default_value
        }
    """

    type: AvroArrayTypeLiteral  # noqa: VNE003,A003 - Value name based on spec
    items: "AvroSchemaTypeDef"
    default: Any  # NotRequired


AvroMapTypeLiteral = Literal["map"]


class AvroMapTypeDef(TypedDict, total=False):
    """Array schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": "map",
            "values": schema,
            "default": default_value
        }
    """

    type: AvroMapTypeLiteral  # noqa: VNE003,A003 - Value name based on spec
    values: "AvroSchemaTypeDef"
    default: Any  # NotRequired


AvroUnionTypeDef = list[str]


AvroFixedTypeLiteral = Literal["fixed"]


class AvroFixedTypeDef(TypedDict, total=False):
    """Array schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": "fixed",
            "name": str,
            "namespace": str,
            "aliases": list[str],
            "size": int
        }
    """

    type: AvroFixedTypeLiteral  # noqa: VNE003,A003 - Value name based on spec
    name: str
    namespace: str  # NotRequired
    alias: list[str]  # NotRequired
    size: int


AvroFixedDecimalLogicalTypeLiteral = Literal["decimal"]


class AvroFixedDecimalTypeDef(TypedDict, total=False):
    """Array schema type definition per spec 1.11.1.

    ::

        Schema: {
            "type": "fixed",
            "name": str,
            "namespace": str,
            "aliases": list[str],
            "size": int
        }
    """

    type: AvroFixedTypeLiteral  # noqa: VNE003,A003 - Value name based on spec
    logicalType: AvroFixedDecimalLogicalTypeLiteral
    name: str
    namespace: str  # NotRequired
    alias: list[str]  # NotRequired
    size: int
    scale: int  # NotRequired
    precision: int


AvroSchemaTypeDef = (
    AvroPrimitiveTypeDef
    | AvroRecordTypeDef
    | AvroEnumTypeDef
    | AvroArrayTypeDef
    | AvroMapTypeDef
    | AvroUnionTypeDef
    | AvroFixedTypeDef
    | AvroFixedDecimalTypeDef
    | str
)

AvroSchemaTypeAlias = Union[
    AvroPrimitiveTypeDef,
    AvroRecordTypeDef,
    AvroEnumTypeDef,
    AvroArrayTypeDef,
    AvroMapTypeDef,
    AvroUnionTypeDef,
    AvroFixedTypeDef,
    AvroFixedDecimalTypeDef,
    str,
]
