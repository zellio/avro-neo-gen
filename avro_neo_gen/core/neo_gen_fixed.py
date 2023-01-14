"""Generated FixedSchema base class."""

import contextlib
from array import array
from decimal import ROUND_HALF_UP, Context, Decimal
from typing import Type, TypeVar, Union

from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject
from avro_neo_gen.core.type_defs import AvroFixedDecimalTypeDef, AvroFixedTypeDef

Self = TypeVar("Self", bound="NeoGenFixed")


class NeoGenFixed(AbstractNeoGenObject):
    """Generated FixedSchema base class."""

    __schema__: AvroFixedTypeDef

    def __init__(self, datum: Union[str, bytes, None] = None) -> None:
        """Construct generated fixed class."""
        self._array = array("B")

        if isinstance(datum, str):
            datum = bytes(datum, encoding="utf-8")

        if isinstance(datum, bytes):
            self.bytes = datum

    def __repr__(self) -> str:
        """Repr instance."""
        return f"<{self.__class__.__name__}(bytes={self._array.tolist()})>"

    @property
    def size(self) -> int:
        """Maximum number of stored bytes."""
        return self.canonical_schema["size"]

    @property
    def bytes(self) -> bytes:  # noqa: A003
        """Copy of the internal bytes array."""
        return self._array.tobytes()

    @bytes.setter
    def bytes(self, datum: bytes) -> None:  # noqa: A003
        """Copy of the internal bytes array."""
        self._array = array("B")
        self._array.frombytes(datum[: self.size])

    def encode(self) -> str:
        """Encode internal bytes as utf-8 string."""
        return self._array.tobytes().decode("utf-8")

    @classmethod
    def decode(cls: Type[Self], datum: str) -> Self:
        """Encode internal bytes as utf-8 string."""
        return cls(datum)


class NeoGenFixedDecimal(NeoGenFixed):
    """Generated FixedSchema base class."""

    __schema__: AvroFixedDecimalTypeDef

    def __init__(self, datum: Union[str, bytes, None] = None) -> None:
        """Construct generated fixed class."""
        super().__init__(datum)
        self._decimal_context = Context(prec=self.precision, rounding=ROUND_HALF_UP)

    @property
    def precision(self) -> int:
        """Maximum number of stored bytes."""
        return self.schema["precision"]

    @property
    def scale(self) -> int:
        """Maximum number of stored bytes."""
        with contextlib.suppress(KeyError):
            return self.schema["scale"]
        return 0

    @property
    def schema(self) -> AvroFixedDecimalTypeDef:
        """Avro schema."""
        return self.__class__.__schema__

    def as_decimal(self) -> Decimal:
        """Cast instance to decimal.Decimal instance."""
        unscaled_int = int.from_bytes(bytes=self.bytes, byteorder="big", signed=True)
        decimal = self._decimal_context.create_decimal(unscaled_int)
        scale = self._decimal_context.create_decimal(self.scale)
        return decimal / 10**scale

    def from_decimal(self, other: Decimal) -> None:
        """Cast instance to decimal.Decimal instance."""
        normal_other = self._decimal_context.create_decimal(other)
        scale = self._decimal_context.create_decimal(self.scale)
        unscaled_other = int(10**scale * normal_other)
        self.bytes = unscaled_other.to_bytes(length=self.size, byteorder="big", signed=True)
