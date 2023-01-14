import ast

from avro_neo_gen.utils import (
    dict_func_merge,
    dict_func_reduce,
    flat_map,
    pyast_load_name,
    pyast_store_name,
)


class TestUtils:
    def test_pyast_load_name(self) -> None:
        assert ast.dump(pyast_load_name("Foo")) == "Name(id='Foo', ctx=Load())"

    def test_pyast_store_name(self) -> None:
        assert ast.dump(pyast_store_name("Foo")) == "Name(id='Foo', ctx=Store())"

    def test_flat_map(self) -> None:
        def identity(value: list[int]) -> list[int]:
            return value

        assert [1, 2, 3] == flat_map(identity, [[1], [2], [3]])

    def test_dict_func_merge(self) -> None:
        assert {"a": {1, 2, 3}, "b": {1, 2}} == dict_func_merge(
            set.union, {"a": {1}, "b": {1}}, {"a": {2, 3}, "b": {1, 2}}
        )

    def test_dict_func_reduce(self) -> None:
        assert {"a": {1, 2, 3}, "b": {1, 2}} == dict_func_reduce(
            set.union,
            [
                {"a": {1}, "b": {1}},
                {"a": {2, 3}, "b": {1, 2}},
                {"a": {3}},
            ],
        )
