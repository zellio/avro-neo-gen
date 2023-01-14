import json
from typing import Callable, Optional

import avro.schema
import pytest
from avro.schema import (
    ArraySchema,
    Field,
    MapSchema,
    PrimitiveSchema,
    RecordSchema,
    UnionSchema,
)

from avro_neo_gen.avro_schema import AvroSchema


class TestAvroSchema:
    def test___init__(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[RecordSchema] = AvroSchema(schema=avro_record_schema)

        assert avro_schema is not AvroSchema(schema=avro_schema)
        assert avro_schema.schema is AvroSchema(schema=avro_schema).schema

        with pytest.raises(TypeError):
            AvroSchema(["weird-type"])

    def test___getattr__(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[RecordSchema] = AvroSchema(schema=avro_record_schema)

        assert avro_schema.fields == avro_record_schema.fields
        assert avro_schema.doc == avro_record_schema.doc

    def test___eq__(
        self,
        avro_primitive_schema_factory: Callable[[str], PrimitiveSchema],
    ) -> None:
        avro_primitive_string = avro_primitive_schema_factory("string")
        avro_schema: AvroSchema[PrimitiveSchema] = AvroSchema(schema=avro_primitive_schema_factory("string"))

        assert avro_schema == avro_primitive_string
        assert avro_schema == AvroSchema(schema=avro_primitive_string)
        assert avro_schema != avro_primitive_string.to_canonical_json()

    def test___repr__(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[RecordSchema] = AvroSchema(schema=avro_record_schema)

        assert str(avro_schema) == "<AvroSchema(RecordSchema(com.acme.User))>"

    def test___iter__(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[RecordSchema] = AvroSchema(schema=avro_record_schema)

        assert list(iter(avro_schema)) == list(avro_schema.contained_schemas())

    def test_contained_schemas(self, avro_record_schema: RecordSchema) -> None:
        avro_schema: AvroSchema[RecordSchema] = AvroSchema(schema=avro_record_schema)
        for field in avro_schema.fields:
            assert field.type in list(avro_schema.contained_schemas())

        field = avro_schema.fields[0]
        avro_field: AvroSchema[Field] = AvroSchema(field)
        assert list(avro_field.contained_schemas()) == [AvroSchema(avro_field.type)]

        array_json = json.dumps({"type": "array", "items": "long"})
        array_schema = avro.schema.parse(array_json)
        avro_array: AvroSchema[ArraySchema] = AvroSchema(array_schema)
        assert list(avro_array.contained_schemas()) == [array_schema.items]

        map_json = json.dumps({"type": "map", "values": "long"})
        map_schema = avro.schema.parse(map_json)
        avro_map: AvroSchema[MapSchema] = AvroSchema(map_schema)
        assert list(avro_map.contained_schemas()) == [avro_map.values]

        union_json = json.dumps(["long", "string"])
        union_schema = avro.schema.parse(union_json)
        avro_union: AvroSchema[UnionSchema] = AvroSchema(union_schema)
        assert list(avro_union.contained_schemas()) == avro_union.schemas

    def test_properties(
        self,
        avro_primitive_schema_factory: Callable[[str, Optional[str]], PrimitiveSchema],
        avro_record_schema: RecordSchema,
    ) -> None:
        avro_primitive_string = avro_primitive_schema_factory("string", None)
        avro_schema: AvroSchema[PrimitiveSchema] = AvroSchema(schema=avro_primitive_schema_factory("string", None))
        assert avro_schema.schema == avro_primitive_string
        assert not avro_schema.is_named
        assert not avro_schema.is_container
        assert avro_schema.name == None
        assert avro_schema.namespace == None
        assert avro_schema.namespace_components == []
        assert avro_schema.fullname == None
        assert avro_schema.fullname_components == []

        avro_schema = AvroSchema(schema=avro_record_schema)
        assert avro_schema.schema == avro_record_schema
        assert avro_schema.is_named
        assert avro_schema.is_container
        assert avro_schema.name == "User"
        assert avro_schema.namespace == "com.acme"
        assert avro_schema.namespace_components == ["com", "acme"]
        assert avro_schema.fullname == "com.acme.User"
        assert avro_schema.fullname_components == ["com", "acme", "User"]

        avro_schema = AvroSchema(schema=avro_record_schema.fields[0])
        assert avro_schema.schema == avro_record_schema.fields[0]
        assert not avro_schema.is_named
        assert avro_schema.is_container
        assert avro_schema.name is None
        assert avro_schema.namespace is None
        assert avro_schema.namespace_components == []
        assert avro_schema.fullname is None
        assert avro_schema.fullname_components == []
