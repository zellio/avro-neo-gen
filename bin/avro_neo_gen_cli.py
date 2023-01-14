"""Command line utility for Avro NeoGen."""

import sys
from pathlib import Path

import click
import structlog

from avro_neo_gen.compiler.compile_parser_namespace_map import (
    compile_parser_namespace_map,
)
from avro_neo_gen.lexer.read_path import read_path
from avro_neo_gen.linker import emit_linker_file_map, link_module
from avro_neo_gen.parser.parse_schema import parse_schema

from .configure_logging import configure_logging

logger = structlog.get_logger(__name__)


def _rmtree(directory: Path) -> None:
    for path in directory.iterdir():
        if path.is_dir():
            _rmtree(path)
            continue
        path.unlink()
    return directory.rmdir()


@click.group()
@click.option(
    "-l",
    "--log-level",
    default="info",
    show_default=True,
    type=click.Choice(["critical", "error", "warning", "info", "debug"], case_sensitive=False),
    envvar="AVRO_NEOGEN_LOG_LEVEL",
    help="Log level",
)
@click.option(
    "-L",
    "--log-format",
    default="plain",
    show_default=True,
    type=click.Choice(["plain", "json"], case_sensitive=False),
    envvar="AVRO_NEOGEN_LOG_FORMAT",
    help="Log format",
)
def avro_neo_gen(log_level: str, log_format: str) -> None:
    """Avro NeoGen: Typed code generation for Avro schemas and protocols."""
    configure_logging(log_level.upper(), log_format.lower())


@avro_neo_gen.command()
def list_drivers() -> None:
    """List provided Avro protocol drivers."""
    ignored_stems = ("__init__", "abstract_avro_driver", "avro_driver_type", "driver_proxy")
    source_base_path = Path(__file__).parent.parent
    driver_module_path = source_base_path / "avro_neo_gen" / "core" / "driver"

    click.echo("Supported Avro drivers:")
    for file_stem in (path.stem for path in driver_module_path.glob("*.py")):
        if file_stem in ignored_stems:
            continue
        click.echo(f" - {file_stem}")


@avro_neo_gen.command()
@click.option(
    "-a",
    "--avro-source-directory",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    envvar="AVRO_NEOGEN_COMPILE_SOURCE_DIRECTORY",
    help="Directory which contains Avro schema and protocol definitions.",
)
@click.option(
    "-p",
    "--python-target-directory",
    default="./build",
    show_default=True,
    type=click.Path(path_type=Path),
    required=True,
    envvar="AVRO_NEOGEN_COMPILE_TARGET_DIRECTORY",
    help="Base directory to write out generated file tree",
)
@click.option(
    "-D",
    "--avro-driver",
    default="apache_avro_binary_driver",
    show_default=True,
    required=True,
    envvar="AVRO_NEOGEN_COMPILE_DRIVER",
    help="Driver for managing avro data in generated code.",
)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    envvar="AVRO_NEOGEN_COMPILE_DRY_RUN",
    help="Generate code without writing files to disk.",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    show_default=True,
    default=False,
    envvar="AVRO_NEOGEN_COMPILE_FORCE",
    help="Force generation of Python library.",
)
def compile(  # noqa: A001
    avro_source_directory: Path,
    python_target_directory: Path,
    avro_driver: str,
    dry_run: bool,
    force: bool,
) -> None:
    """Compile Avro schema files into a typed Python module."""
    logger.debug("Lexing Avro schema files")
    schemas = read_path(path=avro_source_directory)

    logger.debug("Parsing Avro schemas")
    parser_namespace_map = parse_schema(schemas)

    logger.debug("Compiling Avro namespace tree")
    compiler_namespace_map = compile_parser_namespace_map(parser_namespace_map)

    logger.debug("Linking generated Python module")
    module = link_module(namespace_map=compiler_namespace_map)

    if dry_run:
        logger.info("dry_run = True ... exiting.")
        return

    warning_message = f"Target build directory '{python_target_directory}' exists"
    if python_target_directory.exists():
        if force:
            logger.warning(f"{warning_message}, deleting due to force = True.")
            _rmtree(python_target_directory)
        else:
            logger.error(f"{warning_message}, bailing out due to force = False. ")
            sys.exit(1)

    logger.info("Writing compiled Python module.")
    emit_linker_file_map(linker_file_map=module, base_path=python_target_directory)
