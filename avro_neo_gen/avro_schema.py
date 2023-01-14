"""Wrapper class for :class:`avro.schema.Schema`.

See class docstring for details.
"""

from typing import Any, Generic, Iterator, Optional, TypeVar, Union

from avro.schema import (
    ArraySchema,
    Field,
    MapSchema,
    NamedSchema,
    RecordSchema,
    Schema,
    UnionSchema,
)

T = TypeVar("T", bound=Schema | Field)
Self = TypeVar("Self", bound="AvroSchema")


class AvroSchema(Generic[T]):
    """Wrapper class for Apache Avro Schema types.

    Provide additional functionality for :class:`avro.schema.Schema`.

    :class:`AvroSchema` extends the Apache Avro interface to smooth out
    differences in the underlying types so the are easier to operate on.

    Importantly :class:`AvroSchema` guarantees that `name` and `namespace` are
    safe to call, returning `None` when the field is missing.

    :param schema: An :class:`avro.schema.Schema` instance or an
        :class:`AvroSchema` instance to be wrapped.
    :type schema: Union[:class:`AvroSchema`, :class:`T`]
    :raises TypeError: If provided schema

    .. note:: Class can be safely called on :class:`AvroSchema`, which will
        return a new instance which re-wraps the previously wrapped value.
    """

    def __init__(self, schema: T) -> None:
        """Initialize :class:`AvroSchema`."""
        match schema:
            case AvroSchema():
                self._schema: T = schema._schema
            case Schema() | Field():  # type: ignore
                self._schema = schema
            case _:
                raise TypeError from None

    def __getattr__(self, name: str) -> Any:
        """Delegate missing attributes to ``self.schema``.

        :param name: Field name
        :type name: ``str``
        :rtype: :class:`typing.Any`

        .. note:: Wraps internal values in :class:`AvroSchema` before
            returning if the value is an :class:`avro.schema.Schema`.
        """
        attr = getattr(self.schema, name)
        if isinstance(attr, Schema | Field):
            return AvroSchema(attr)

        if isinstance(self.schema, RecordSchema) and name == "fields":
            return list(map(AvroSchema, attr))

        if isinstance(self.schema, UnionSchema) and name == "schemas":
            return list(map(AvroSchema, attr))

        return attr

    def __eq__(self, other: object) -> bool:
        """Delegate equality to contained schema.

        :param other: :class:`Object` to be compared against.
        :type other: :class:`Object`
        :return: `True` if contained :class:`avro.schema.Schema` is equal to
            ``other`` or the :class:`avro.schema.Schema` contained therein.
        :rtype: ``bool``
        """
        match other:  # noqa: R503 - Base case raises type error
            case AvroSchema():
                return self.schema == other.schema
            case Schema() | Field():  # type: ignore
                return self.schema == other
        return False

    def __repr__(self) -> str:
        """Instance repr."""
        return f"<AvroSchema({self.schema.__class__.__name__}({self.fullname or self.name or ''}))>"

    def __iter__(self) -> Iterator[Self]:
        """Iterate over ``self.contained_schemas()``.

        :return: Value returned by calling ``self.contained_schemas``.
        :rtype: Iterator[:class:`AvroSchema`]
        """
        return self.contained_schemas()

    def contained_schemas(self) -> Iterator[Self]:
        """Iterate over type definitions contained within schema.

        This method is only really valid on instances for which,
        ``self.is_container`` is `True`.

        :returns: Iterable across contained schemas
        :rtype: ``Iterable[AvroSchema]``

        .. note:: Wraps internal values in instances of :class:`AvroSchema`

        """
        contained_schemas: list[Union[Schema, Field]] = []
        match self.schema:
            case RecordSchema():  # type: ignore
                contained_schemas = [field.type for field in self.fields]
            case Field():  # type: ignore
                contained_schemas = [self.type]
            case ArraySchema():  # type: ignore
                contained_schemas = [self.items]
            case MapSchema():  # type: ignore
                contained_schemas = [self.values]
            case UnionSchema():  # type: ignore
                contained_schemas = self.schemas

        yield from contained_schemas

    @property
    def schema(self) -> T:
        """Contained Avro schema.

        :return: ``self._schema``
        :rtype: ``avro.schema.Schema``
        """
        return self._schema

    @property
    def is_named(self) -> bool:
        """Contained schema type check as object property.

        :return: `True` if contained :class:`avro.schema.Schema` is an
            instance of :class:`avro.schema.NamedSchema`, `Flase` otherwise.
        :rtype: bool
        """
        return isinstance(self.schema, NamedSchema)

    @property
    def is_container(self) -> bool:
        """Contained schema type check as object property.

        :return: `True` if contained :class:`avro.schema.Schema` can contain
            other type definitions, `False` otherwise.
        :rtype: bool
        """
        return isinstance(self.schema, RecordSchema | Field | ArraySchema | MapSchema | UnionSchema)

    @property
    def name(self) -> Optional[str]:
        """Safe proxy to ``self.schema.name``.

        :return: Contained schema name if it is an
            :class:`avro.schema.NamedSchema`, None otherwise.
        :rtype: Optional[str]
        """
        if self.is_named:
            return self.schema.name
        return None

    @property
    def namespace(self) -> Optional[str]:
        """Safe proxy to ``self.schema.namespace``.

        :return: Contained schema namespace if it is an
            :class:`avro.schema.NamedSchema`, None otherwise.
        :rtype: Optional[str]
        """
        if self.is_named:
            return self.schema.namespace
        return None

    @property
    def namespace_components(self) -> list[str]:
        """Split ``self.namespace`` on standard delimiter: `.`.

        :return: Components of namespace as a list, empty if there is no
            namespace.
        :rtype: list[str]
        """
        if self.namespace:
            return self.namespace.split(".")
        return []

    @property
    def fullname(self) -> Optional[str]:
        """Safe proxy to ``self.schema.fullname``.

        :return: Contained schema fullname if it is an
            :class:`avro.schema.NamedSchema`, None otherwise.
        :rtype: Optional[str]
        """
        if self.is_named:
            return self.to_canonical_json()["name"]
        return None

    @property
    def fullname_components(self) -> list[str]:
        """Split self.fullname on standard delimiter: .

        :return: Components of fullname as a list, empty if there is no
            fullname.
        :rtype: list[str]
        """
        if self.fullname:
            return self.fullname.split(".")
        return []
