import json

import avro.schema

from avro_neo_gen.parser.parse_schema import parse_schema


class TestParserParseSchema:
    def test_parse_schema(self, avro_record_schema_json: str) -> None:
        schema = json.loads(avro_record_schema_json)
        com_record = avro.schema.parse(json.dumps(schema | {"namespace": "com.acme", "name": "ComTest"}))
        org_record = avro.schema.parse(json.dumps(schema | {"namespace": "org.acme", "name": "OrgTest"}))

        parser_namespace_map = parse_schema([com_record, org_record])

        assert "com.acme" in parser_namespace_map
        assert parser_namespace_map["com.acme"][-1] == com_record

        assert "org.acme" in parser_namespace_map
        assert parser_namespace_map["org.acme"][-1] == org_record

        assert parser_namespace_map["org.acme"][:-1] == parser_namespace_map["com.acme"][:-1]

    def test_parse_schema_alternate_embeds(self, avro_record_schema_json: str) -> None:
        schema = json.loads(avro_record_schema_json)
        com_record = avro.schema.parse(
            json.dumps(
                schema
                | {
                    "name": "ComTest",
                    "namespace": "com.acme",
                    "fields": [{"name": "org_test", "type": schema | {"name": "OrgTest", "namespace": "org.acme"}}],
                }
            )
        )
        org_record = com_record.fields[0].type

        parser_namespace_map = parse_schema([com_record])

        assert "com.acme" in parser_namespace_map
        assert parser_namespace_map["com.acme"][-1] == com_record
        assert org_record not in parser_namespace_map["com.acme"]

        assert "org.acme" in parser_namespace_map
        assert parser_namespace_map["org.acme"][-1] == org_record
