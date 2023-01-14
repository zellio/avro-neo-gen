from typing import Any
from unittest.mock import Mock, patch

from avro_neo_gen.core.utils import record_builder_internal


class TestCoreUtils:
    @patch("inspect.currentframe", return_value=None)
    def test_record_builder_internal_no_current_frame(self, _: Any) -> None:
        def _test_func(field_one: int, field_two: str) -> dict:
            return record_builder_internal()

        assert _test_func(10, "hello test") == {}

    @patch("inspect.currentframe", return_value=Mock(f_back=None))
    def test_record_builder_internal_no_fback(self, _: Any) -> None:
        def _test_func(field_one: int, field_two: str) -> dict:
            return record_builder_internal()

        assert _test_func(10, "hello test") == {}

    def test_record_builder_internal(self) -> None:
        def _test_func(field_one: int, field_two: str) -> dict:
            return record_builder_internal()

        assert _test_func(10, "hello test") == {"field_one": 10, "field_two": "hello test"}
