from types import ModuleType

from avro_neo_gen.core.neo_gen_record import NeoGenRecord


class TestCoreNeoGenRecord:
    def test_neo_gen_record_base(self) -> None:
        neo_gen_record = NeoGenRecord()
        assert neo_gen_record._datum == {}

    def test_neo_gen_record(self, neo_gen_record_module: ModuleType) -> None:
        User = neo_gen_record_module.User
        assert issubclass(User, NeoGenRecord)

        alice = User(name="alice", favorite_number=10, favorite_color=None)

        assert isinstance(alice, NeoGenRecord)
        assert alice._datum == {"name": "alice", "favorite_number": 10, "favorite_color": None}

    def test___repr__(self, neo_gen_record_module: ModuleType) -> None:
        User = neo_gen_record_module.User
        assert (
            str(User(name="alice", favorite_number=10, favorite_color=None))
            == "<User(datum={'name': 'alice', 'favorite_number': 10, 'favorite_color': None})>"
        )

    def test_encode(self, neo_gen_record_module: ModuleType) -> None:
        User = neo_gen_record_module.User
        assert User(name="alice", favorite_number=10, favorite_color=None).encode() == {
            "name": "alice",
            "favorite_number": 10,
            "favorite_color": None,
        }

    def test_decode(self, neo_gen_record_module: ModuleType) -> None:
        User = neo_gen_record_module.User
        alice = User.decode({"name": "alice", "favorite_number": 10, "favorite_color": None})
        assert alice.name == "alice"
        assert alice.favorite_number == 10
        assert alice.favorite_color == None

    def test_generated_properties(self, neo_gen_record_module: ModuleType) -> None:
        User = neo_gen_record_module.User
        alice = User(name="Alice", favorite_number=42, favorite_color="#28a99e")

        assert alice.name == "Alice"
        assert alice.favorite_number == 42
        assert alice.favorite_color == "#28a99e"

        alice.favorite_color = "teal"

        assert alice.encode()["favorite_color"] == "teal"
