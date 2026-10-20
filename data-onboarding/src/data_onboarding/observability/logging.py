import logging
import sys

import structlog

from data_onboarding.core.settings import get_settings

def setup_logger() -> structlog.stdlib.BoundLogger:
    settings = get_settings()
    

    '''Configures structured logging based on application settings.'''
    log_level = getattr(logging, settings.secrets.log_level.upper(), logging.INFO)

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.secrets.env == "prod":
        # render JSON for container logs/k8s
        renderer = structlog.processors.JSONRenderer()
    else:
        # readable colored output for local development
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    return structlog.get_logger()


# pre-configured logger instance
log = setup_logger()