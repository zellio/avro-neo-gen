"""Parse Avro schemas from a directory."""

import json
from pathlib import Path
from typing import Iterator, Union

import avro.schema
from avro.schema import Schema

__all__ = ["read_path"]


def read_path(path: Union[str, Path], extension: str = "avsc", encoding: str = "utf-8") -> Iterator[Schema]:
    """Read avro schema files into memory.

    :param path: Source directory containing avro schema files.
    :type path: Union[str, Path]
    :param extension: Extension of Avro schema files to be lexed, defaults to ``"avsc"``.
    :type extension: str
    :param encoding: Text encoding of Avro schema files, defaults to ``"utf-8"``.
    :type encoding: str
    :return: A stream of avro schema files loaded into memory as Apache Avro objects.
    :rtype: Iterator[Schema]:

    Conceptually, one schema is a "token" for our compiler.

    .. note:: If the extension of the ``path`` parameter matches the
        ``extension`` parameter then ``read_path`` will assume it is lexing a
        single file, otherwise it will search for all files under ``path``
        with the provided ``extension``.
    """
    path = Path(path)

    if path.suffix == f".{extension}":
        avro_files = [path]
    else:
        avro_files = sorted(path.glob(f"**/*.{extension}"))

    for avro_file in avro_files:
        avro_text = avro_file.read_text(encoding=encoding)
        avro_json = json.loads(avro_text)
        match avro_json:
            case str():
                raise NotImplementedError
            case list():
                raise NotImplementedError
            case dict():
                yield avro.schema.parse(avro_text)
            case _:
                raise NotImplementedError
