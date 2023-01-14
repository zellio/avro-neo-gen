"""Untility functions."""

from ast import AST, Load, Module, Name, Store
from functools import reduce
from typing import Callable, Iterable, TypeVar

__all__ = [
    "dict_func_merge",
    "dict_func_reduce",
    "flat_map",
    "flat_map_gen",
    "pyast_load_name",
    "pyast_store_name",
]


A = TypeVar("A")  # noqa: VNE001 Type variable, length dictated by industry convention
B = TypeVar("B")  # noqa: VNE001 Type variable, length dictated by industry convention


def pyast_module(body: list[AST]) -> Module:
    return Module(type_ignores=[], body=body)


def pyast_load_name(name: str) -> Name:
    """Generate a load contxt ast.Name value."""
    return Name(id=name, ctx=Load())


def pyast_store_name(name: str) -> Name:
    """Generate a store contxt ast.Name value."""
    return Name(id=name, ctx=Store())


def flat_map_gen(func: Callable[[A], Iterable[B]], values: Iterable[A]) -> Iterable[B]:
    """Perform very common flat-map operation.

    flat_map returns a new iterable by applying func to each value of values
    and flattening the result by one level:

        def func(x):
            return [1, 2, 3]

        flat_map(func, ["a", "b", "c"]) -> generator(1, 2, 3, 1, 2, 3, 1, 2, 3)

    """
    for value in values:
        yield from func(value)


def flat_map(func: Callable[[A], list[B]], values: Iterable[A]) -> list[B]:
    """Perform very common flat-map operation.

    flat_map returns a new iterable by applying func to each value of values
    and flattening the result by one level:

        def func(x):
            return [1, 2, 3]

        flat_map(func, ["a", "b", "c"]) -> generator(1, 2, 3, 1, 2, 3, 1, 2, 3)

    """
    return list(flat_map_gen(func, values))


def dict_func_merge(reducer: Callable[[B, B], B], left: dict[A, B], right: dict[A, B]) -> dict[A, B]:
    """Deep merge two dicts, joining the values by `reducer'."""
    new_map: dict[A, B] = {}
    for key in set(left.keys()).union(right.keys()):
        if key not in left:
            new_map[key] = right[key]
        elif key not in right:
            new_map[key] = left[key]
        else:
            new_map[key] = reducer(left[key], right[key])
    return new_map


def dict_func_reduce(reducer: Callable[[B, B], B], dicts: Iterable[dict[A, B]]) -> dict[A, B]:
    """Deep merge a list of dicts, joining the values by `reducer'."""
    return reduce(lambda left, right: dict_func_merge(reducer, left, right), dicts, {})
