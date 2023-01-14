"""Configure structlog root logger."""

import logging
from typing import Union

import structlog

__all__ = ["configure_logging"]


def configure_logging(log_level: str = "INFO", log_format: str = "plain") -> None:
    """Configure stdlib and structlog root logger.

    :param log_level: Log level for loggers, must be one of: "critical",
        "error", "warning", "info", or "debug", defaults to "info".
    :type log_level: str
    :param log_format: Log format for loggers, must be one of: plain, or json,
        defaults to "plain".
    :type log_format: str
    """
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),  # stack_info = True
        structlog.processors.format_exc_info,  # exc_info = True
    ]

    processors = [
        structlog.stdlib.filter_by_level,
        *shared_processors,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        context_class=dict,
        processors=processors,  # type: ignore
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    renderer: Union[structlog.dev.ConsoleRenderer, structlog.processors.JSONRenderer]
    if log_format and log_format.lower() == "plain":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    handler = logging.StreamHandler()
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,  # type: ignore
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                renderer,
            ],
        ),
    )

    logging.captureWarnings(True)

    logging.basicConfig(
        format="%(message)s",
        handlers=[handler],
        level=log_level,
        force=True,
    )
