"""Generated Enum schema base class."""

from functools import total_ordering
from typing import Generator, Type, TypeVar

from avro_neo_gen.core.abstract_neo_gen_object import (
    AbstractNeoGenObject,
    AbstractNeoGenObjectMeta,
)
from avro_neo_gen.core.neo_gen_error import (
    NeoGenAttributeError,
    NeoGenKeyError,
    NeoGenValueError,
)
from avro_neo_gen.core.type_defs import AvroEnumTypeDef


class NeoGenEnumTypeMeta(type):
    """Generated Enum schema metaclass."""

    __schema__: AvroEnumTypeDef

    def _is_valid_symbol(cls, symbol: str) -> bool:
        """Check if a given symbol is a valid Enum value.

        :return: True of symbol is in schema symbols, False otherwise
        :rtype: bool
        """
        return symbol in getattr(cls, "__schema__", {"symbols": []})["symbols"]

    def __getattr__(cls, symbol: str) -> "NeoGenEnum":
        """Emulate python Enema class __getattr__."""
        if cls._is_valid_symbol(symbol):
            return cls(symbol)
        raise NeoGenAttributeError from None

    def __getitem__(cls, symbol: str) -> "NeoGenEnum":
        """Emulate python Enum class __getitem__."""
        try:
            return cls.__getattr__(symbol)
        except AttributeError:
            raise NeoGenKeyError from None

    def __iter__(cls) -> Generator["NeoGenEnum", None, None]:
        """Return symbols in definition order."""
        return (cls[symbol] for symbol in cls.__schema__.get("symbols", []))

    def __len__(cls) -> int:
        """Return the number of symbols."""
        return len(cls.__schema__.get("symbols", []))

    def __reversed__(cls) -> Generator["NeoGenEnum", None, None]:
        """Return symbols in reverse schema order."""
        return (cls[symbol] for symbol in reversed(cls.__schema__.get("symbols", [])))


class NeoGenEnumType(metaclass=NeoGenEnumTypeMeta):
    """Base generated NeoGenEnum."""

    # Empty Enum schema, this needs to be defined to break __getattr__ loop in
    # type initialization.
    __schema__: AvroEnumTypeDef = AvroEnumTypeDef(
        type="enum",
        name="NeoGenEnum",
        namespace="avro_neo_gen.core",
        symbols=[],
    )


class NeoGenEnumMeta(AbstractNeoGenObjectMeta, NeoGenEnumTypeMeta):  # type: ignore
    """Merged NeoGenEnum meta classes."""

    pass


Self = TypeVar("Self", bound="NeoGenEnum")


@total_ordering
class NeoGenEnum(AbstractNeoGenObject, NeoGenEnumType, metaclass=NeoGenEnumMeta):  # type: ignore
    """Generated EnumSchema base class."""

    __schema__: AvroEnumTypeDef

    def __init__(self, datum: str) -> None:
        """Construct generated fixed class."""
        self._datum = datum

    def __repr__(self) -> str:
        """Repr instance."""
        return f"<{self.__class__.__name__}(symbol={self._datum})>"

    def __eq__(self, other: object) -> bool:
        """Evaluate equality.

        :return: True if instances are the same type with the same contained _datum, False otherwise.
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            return self._datum.__eq__(other._datum)
        return False

    def __lt__(self, other: object) -> bool:
        """Evaluate value ordering based on schema rank.

        :return: True if self._datum appears in symbol list before other._datum, False otherwise.
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            self_index = self.canonical_schema["symbols"].index(self._datum)
            other_index = self.canonical_schema["symbols"].index(other._datum)
            return self_index.__lt__(other_index)
        return True

    def encode(self) -> str:
        """Encode enum value as its symbol name."""
        return str(self._datum)

    @classmethod
    def decode(cls: Type[Self], datum: str) -> Self:
        """Ingest datum to internal state, munging based on spec."""
        if not cls._is_valid_symbol(datum):  # type: ignore
            raise NeoGenValueError from None
        return getattr(cls, datum)
