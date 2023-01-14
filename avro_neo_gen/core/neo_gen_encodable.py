"""Generated Avro NeoGen type Protocol for encodable schemas."""

from io import BufferedIOBase
from typing import Any, Protocol, Type, TypeVar

from avro_neo_gen.core.driver.driver_proxy import DriverProxy

Self = TypeVar("Self", bound="NeoGenEncodable")


class NeoGenEncodable(Protocol):
    """Generated Avro NeoGen type Protocol for encodable schemas."""

    __driver_proxy__: DriverProxy

    @classmethod
    def read(cls: Type[Self], source: BufferedIOBase) -> Self:
        """Read encoded avro schema via DriverProxy into a new typed instance."""
        ...

    def write(self, target: BufferedIOBase) -> None:
        """Write instance values into an  encoded avro schema via DriverProxy."""
        ...

    def encode(self) -> Any:
        """Cast typed entity to representational data per caonical_schema."""
        ...

    def encode_json(self) -> str:
        """Encode self.encode as json string."""
        ...

    @classmethod
    def decode(cls, datum: Any) -> Any:
        """Ingest datum to internal state, munging based on spec."""
        ...

    @classmethod
    def decode_json(cls: Type[Self], datum: str) -> Self:
        """Decode datum as a json string."""
        ...
