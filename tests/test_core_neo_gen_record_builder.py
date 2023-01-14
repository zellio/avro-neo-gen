from types import ModuleType

from avro_neo_gen.core.abstract_neo_gen_record_builder import (
    AbstractNeoGenRecordBuilder,
)
from avro_neo_gen.core.neo_gen_record import NeoGenRecord


class TestCoreNeoGenRecord:
    def test_neo_gen_record_builder(self, neo_gen_record_module: ModuleType) -> None:
        UserBuilder = neo_gen_record_module.UserBuilder
        assert issubclass(UserBuilder, AbstractNeoGenRecordBuilder)

        alice = UserBuilder().name("alice").favorite_number(10).favorite_color(None).build()

        assert isinstance(alice, NeoGenRecord)
        assert alice._datum == {"name": "alice", "favorite_number": 10, "favorite_color": None}
