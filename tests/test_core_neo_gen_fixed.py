from decimal import Decimal
from types import ModuleType

from avro_neo_gen.core.neo_gen_fixed import NeoGenFixed, NeoGenFixedDecimal


class TestCoreNeoGenFixed:
    def test_neo_gen_fixed(self, neo_gen_fixed_module: ModuleType) -> None:
        MD5 = neo_gen_fixed_module.MD5
        assert issubclass(MD5, NeoGenFixed)
        assert isinstance(MD5(b"01234567890123456789"), NeoGenFixed)

        assert MD5(b"01234567890123456789").bytes == b"0123456789012345"
        assert MD5(b"01234567890123456789").size == len(MD5(b"01234567890123456789").bytes)
        assert MD5("01234567890123456789").bytes == bytes("0123456789012345", encoding="utf-8")

        md5 = MD5(b"01234567890123456789")
        md5.bytes = b"0"
        assert md5.bytes == b"0"

    def test___repr__(self, neo_gen_fixed_module: ModuleType) -> None:
        MD5 = neo_gen_fixed_module.MD5
        assert str(MD5(b"0123")) == "<MD5(bytes=[48, 49, 50, 51])>"

    def test_encode(self, neo_gen_fixed_module: ModuleType) -> None:
        MD5 = neo_gen_fixed_module.MD5
        assert MD5(b"0123").encode() == "0123"

    def test_decode(self, neo_gen_fixed_module: ModuleType) -> None:
        MD5 = neo_gen_fixed_module.MD5
        assert MD5.decode("1534").bytes == b"1534"

    def test_neo_gen_fixed_decimal(self, neo_gen_fixed_decimal_module: ModuleType) -> None:
        FixNum = neo_gen_fixed_decimal_module.FixNum

        assert issubclass(FixNum, NeoGenFixedDecimal)

        fixnum = FixNum(b"5134")
        assert isinstance(fixnum, NeoGenFixed)
        assert isinstance(fixnum, NeoGenFixedDecimal)

        assert fixnum.precision == 4
        assert fixnum.scale == 2

        del FixNum.__schema__["scale"]
        assert fixnum.scale == 0

    def test_as_decimal(self, neo_gen_fixed_decimal_module: ModuleType) -> None:
        FixNum = neo_gen_fixed_decimal_module.FixNum
        fixnum = FixNum("5134")
        assert fixnum.as_decimal() == Decimal("8.924E+6")

    def test_from_decimal(self, neo_gen_fixed_decimal_module: ModuleType) -> None:
        FixNum = neo_gen_fixed_decimal_module.FixNum
        fixnum = FixNum(b"5134")

        fixnum.from_decimal(10)
        assert fixnum.bytes == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xe8"
        assert fixnum.as_decimal() == 10
