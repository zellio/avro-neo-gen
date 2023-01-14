### Configuration file for the Sphinx documentation builder.

# flake8: noqa
# type: ignore


### Add project path to load path

from pathlib import Path
from sys import path as sys_path

conf_filepath = Path(__file__).absolute()
project_root = str(conf_filepath.parent.parent.parent)

if project_root not in sys_path:
    sys_path.append(project_root)


### Configure sphinx

project = "Avro NeoGen"
copyright = "2023, Zachary Elliott"
author = "Zachary Elliott"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.viewcode",
    "sphinx_click",
]

myst_enable_extensions = [
    "replacements",
]

templates_path = ["_templates"]
exclude_patterns = []
include_patterns = ["*.md"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
