"""Proxy class for shared Avro driver."""

from importlib import import_module
from io import BufferedIOBase
from types import ModuleType
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

from avro_neo_gen.core.driver.abstract_avro_driver import AbstractAvroDriver
from avro_neo_gen.core.neo_gen_error import (
    NeoGenDriverClassNotFound,
    NeoGenDriverLoadFailure,
    NeoGenDriverModuleNotFound,
    NeoGenDriverUnloadedError,
)

if TYPE_CHECKING:
    from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject

S = TypeVar("S", bound="AbstractNeoGenObject")  # noqa: VNE001 - Type variable.


class _Monostate:
    """A monostate is a "conceptual singleton".

    All data members of a monostate are static, so all instances of the
    monostate use the same (static) data.
    """

    __shared_state__: dict[str, Any] = {}

    def __init__(self) -> None:
        self.__dict__ = self.__shared_state__


class DriverProxy(AbstractAvroDriver, _Monostate):
    """Shared sate proxy for Avro driver access."""

    def __init__(self) -> None:
        """Initialize DriverProxy and shared class state."""
        _Monostate.__init__(self)

        if not hasattr(self, "_driver_module"):
            self._driver_module: Optional[ModuleType] = None

        if not hasattr(self, "_driver_class"):
            self._driver_class: Optional[Type] = None

        if not hasattr(self, "_driver"):
            self._driver: Optional[AbstractAvroDriver] = None

    @classmethod
    def load_driver(cls, module_name: str) -> None:
        """Attempt to load the specified driver.

        NB. Assume that bare names are based in avro_neo_gen.core.driver

        :param module_name: Name of the Avro driver module to load
        :type module_name: str
        """
        cls()._load_driver(module_name)

    def _load_driver(self, module_name: str) -> None:
        if "." not in module_name:
            module_name = f"avro_neo_gen.core.driver.{module_name}"

        try:
            self._driver_module = import_module(module_name)
            self._driver_class = next(
                cls
                for cls in map(self._driver_module.__dict__.get, self._driver_module.__all__)
                if isinstance(cls, type) and issubclass(cls, AbstractAvroDriver)
            )
            self._driver = self._driver_class()
        except ModuleNotFoundError as mnfe:
            raise NeoGenDriverModuleNotFound from mnfe

        except StopIteration as sie:
            raise NeoGenDriverClassNotFound from sie

        except Exception as exc:
            raise NeoGenDriverLoadFailure from exc

    @property
    def driver(self) -> AbstractAvroDriver:
        """Safe proxy for self._driver.

        :raises: NeoGenDriverLoadFailure
        :returns: self._driver.
        :rtype: AbstractAvroDriver
        """
        if self._driver is None:
            raise NeoGenDriverUnloadedError
        return self._driver

    def read(self, schema_type: Type[S], source: BufferedIOBase) -> S:
        """Read a single schema from source stream and return a typed instance."""
        return self.driver.read(schema_type=schema_type, source=source)

    def write(self, schema: S, target: BufferedIOBase) -> None:
        """Write a single schema to target stream."""
        self.driver.write(schema=schema, target=target)
