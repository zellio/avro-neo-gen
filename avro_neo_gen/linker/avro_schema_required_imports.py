"""Identify required imports for a AvroSchema."""

from avro.schema import (
    EnumSchema,
    FixedDecimalSchema,
    FixedSchema,
    LogicalSchema,
    PrimitiveSchema,
    RecordSchema,
    Schema,
    UnionSchema,
)

from avro_neo_gen.avro_schema import AvroSchema
from avro_neo_gen.type_defs import LinkerRequiredImports
from avro_neo_gen.utils import dict_func_merge, dict_func_reduce


def _logical_schema_required_imports(avro_schema: AvroSchema[LogicalSchema]) -> LinkerRequiredImports:
    match avro_schema.logical_type:  # noqa: R503 base case raises error
        case "uuid":
            return {"uuid": {"UUID"}}
        case "date":
            return {"datetime": {"date"}}
        case "time-millis" | "time-micros":
            return {"datetime": {"time"}}
        case "timestamp-millis" | "timestamp-micros":
            return {"datetime": {"datetime"}}
        case _:
            raise NotImplementedError


def avro_schema_required_imports(avro_schema: AvroSchema[Schema]) -> LinkerRequiredImports:
    """Identify required imports for a AvroSchema.

    :param avro_schmea: AvroSchema container of the Schema whos required
        imports we are resolving.
    :type avro_schmea: :class:`AvroSchema[:class:`avro.schema.Schema`]`
    :return: Map of namespace to set of classes required by the provided schema.
    :rtype: :class:`LinkerRequiredImports`

    An objects requirements are considered to be the union of its requirements
    and the requirements of all of its contained schemas.

    .. note:: Currently requirement resolution is done from the source schema
        rather than generated AST. This is in large part for ease of linking
        and identification of external dependencies.
    """
    required_imports: LinkerRequiredImports = {}
    match avro_schema.schema:  # noqa: R503 - base case must return / raise
        case PrimitiveSchema():  # type: ignore
            if isinstance(avro_schema.schema, LogicalSchema):
                required_imports = _logical_schema_required_imports(avro_schema)
        case RecordSchema():  # type: ignore
            required_imports = {
                "avro_neo_gen.core": {"AbstractNeoGenRecordBuilder", "NeoGenRecord"},
                "avro_neo_gen.core.utils": {"record_builder_internal"},
            }
        case EnumSchema():  # type: ignore
            required_imports = {"avro_neo_gen.core": {"NeoGenEnum"}}
        case FixedDecimalSchema():  # type: ignore
            required_imports = {"avro_neo_gen.core": {"NeoGenFixedDecimal"}}
        case FixedSchema():  # type: ignore
            required_imports = {"avro_neo_gen.core": {"NeoGenFixed"}}
        case UnionSchema():  # type: ignore
            required_imports = {"typing": {"Union"}}
            if len([schema for schema in avro_schema.schemas if schema.type != "null"]) == 1:
                required_imports = {"typing": {"Optional"}}
        case _:
            raise NotImplementedError

    foreign_contained_schemas = [
        schema
        for schema in avro_schema.contained_schemas()
        if schema.namespace and schema.namespace != avro_schema.namespace
    ]
    if foreign_contained_schemas:
        required_imports = dict_func_reduce(
            set.union,
            [
                required_imports,
                *[{schema.namespace: {schema.name}} for schema in foreign_contained_schemas],
            ],
        )

    if avro_schema.is_named:
        return dict_func_merge(set.union, required_imports, {"collections": {"OrderedDict"}})

    return required_imports
