from typing import Any, Callable
from unittest.mock import patch

import pytest

from avro_neo_gen.core.driver.driver_proxy import DriverProxy, _Monostate
from avro_neo_gen.core.neo_gen_error import (
    NeoGenDriverClassNotFound,
    NeoGenDriverLoadFailure,
    NeoGenDriverModuleNotFound,
    NeoGenDriverUnloadedError,
)


class TestCoreDriverDriverProxy:
    def test__Monostate(self) -> None:
        m1 = _Monostate()
        m2 = _Monostate()

        m1.setting = "test-value"  # type: ignore

        assert m2.setting == "test-value"  # type: ignore
        assert m1 is not m2
        assert m1.setting == m2.setting  # type: ignore

    def test_raises_error_on_unloaded(self) -> None:
        with pytest.raises(NeoGenDriverUnloadedError):
            DriverProxy().driver

    def test_raises_error_on_bad_module(self) -> None:
        with pytest.raises(NeoGenDriverModuleNotFound):
            DriverProxy.load_driver("invalid-path-class")

    def test_raises_error_on_class_load_failure(self) -> None:
        with pytest.raises(NeoGenDriverClassNotFound):
            DriverProxy.load_driver("avro_neo_gen.utils")

    def test_wraps_generic_error(self) -> None:
        with pytest.raises(NeoGenDriverLoadFailure), patch(
            "avro_neo_gen.core.driver.driver_proxy.import_module",
        ) as import_module_mock:
            import_module_mock.side_effect = Exception()
            DriverProxy.load_driver("")

    def test_load_driver(
        self,
        stateless_driver_proxy_factory: Callable[[str], DriverProxy],
    ) -> None:
        _ = stateless_driver_proxy_factory("avro_neo_gen.core.driver.apache_avro_binary_driver")

        d1 = DriverProxy()
        d2 = DriverProxy()

        assert d1 is not d2
        assert d1._driver is d2._driver

    def test_read(self) -> None:
        class MockReader:
            def read(self, schema_type: Any, source: Any) -> str:
                return "test-value"

        driver_proxy = DriverProxy()
        driver_proxy._driver = MockReader()  # type: ignore
        assert driver_proxy.read(None, None) == "test-value"  # type: ignore

    def test_write(self) -> None:
        class MockWriter:
            def write(self, schema: Any, target: Any) -> None:
                self.test_value = schema

        driver_proxy = DriverProxy()
        driver_proxy._driver = MockWriter()  # type: ignore
        driver_proxy.write("test-value", None)  # type: ignore
        assert driver_proxy._driver.test_value == "test-value"  # type: ignore
