"""Generated Builder type protocol."""

from typing import Protocol

from avro_neo_gen.core.abstract_neo_gen_object import AbstractNeoGenObject


class NeoGenBuilder(Protocol):
    """Generated Builder type protocol."""

    def build(self) -> AbstractNeoGenObject:
        """Build the builder target class."""
        ...
