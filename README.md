# Avro Neogene

Typed Python code generation library for [Apache Avro][1] schemas.


## Requirements

Code generation requires `python 3.11` or newer.

Generated code requires `python 3.6` or newer.

> **_NOTE:_** Generated code has no dependencies other than core python
> libraries.


## Installation

First install a copy of `python 3.11` or newer, either via your operating
system's repos or via [pyenv][2]:

```shell
pyenv install 3.11
```

`avro-neo-gen` is primarily a CLI tool, it is easiest to install via [pipx][3]:

```shell
declare python_prefix="$(pyenv prefix 3.11)"
pipx install --python "$python_prefix"/bin/python avro-neo-gen
```

If you would rather install the package manually, you can do so via pip:

```shell
python -m pip install avro-neo-gen
```


## Usage

...


## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/[USERNAME]/avro-neo-gen. This project is intended to be a
safe, welcoming space for collaboration, and contributors are expected to
adhere to the [code of conduct][4].


## Copyright

BSD 3 Clause (New BSD)
Copyright (C) 2022, Zachary Elliott <contact@zell.io>


<!-- Reference links -->

[1]: https://avro.apache.org/ "Apache Avro"
[2]: https://github.com/pyenv/pyenv "pyenv"
[3]: https://pypa.github.io/pipx/ "pipx"
[4]: CODE_OF_CONDUCT.md
