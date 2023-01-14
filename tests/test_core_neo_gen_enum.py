from types import ModuleType

import pytest

from avro_neo_gen.core.neo_gen_enum import NeoGenEnum


class TestCoreNeoGenEnum:
    def test_neo_gen_enum(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        assert issubclass(Suit, NeoGenEnum)
        assert isinstance(Suit.DIAMONDS, NeoGenEnum)

    def test_enum_meta_type__getattr__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit

        assert Suit("DIAMONDS") == Suit.DIAMONDS

        with pytest.raises(AttributeError):
            _ = neo_gen_enum_module.Suit.FOO

    def test_enum_meta_type__getitem__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit

        assert Suit("DIAMONDS") == Suit["DIAMONDS"]

        with pytest.raises(KeyError):
            _ = neo_gen_enum_module.Suit["FOO"]

    def test_enum_meta_type__iter__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        assert list(iter(Suit)) == [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]

    def test_enum_meta_type__len__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        assert len(Suit) == len(Suit("DIAMONDS").canonical_schema["symbols"])

    def test_enum_meta_type__reversed__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        assert list(reversed(Suit)) == [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]

    def test___init__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        suit = Suit("DIAMONDS")
        assert suit._datum == "DIAMONDS"

    def test___repr__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        suit = Suit("DIAMONDS")
        assert str(suit) == "<Suit(symbol=DIAMONDS)>"

    def test___eq__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        assert Suit("DIAMONDS") == Suit("DIAMONDS")
        assert Suit("DIAMONDS") != Suit("HEADTS")
        assert Suit("DIAMONDS") != "DIAMONDS"

    def test___lt__(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit

        assert Suit("DIAMONDS") > Suit("HEARTS")
        assert Suit("DIAMONDS") < Suit("CLUBS")
        assert Suit("DIAMONDS") < "DIAMONDS"
        assert Suit("DIAMONDS") < "HEARTS"
        assert [suit._datum for suit in Suit] == Suit("DIAMONDS").canonical_schema["symbols"]

    def test_encode(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit
        assert Suit("DIAMONDS").encode() == "DIAMONDS"

    def test_decode(self, neo_gen_enum_module: ModuleType) -> None:
        Suit = neo_gen_enum_module.Suit

        assert Suit.HEARTS == Suit.decode("HEARTS")
        with pytest.raises(ValueError):
            Suit.decode("FOO")
