import logging
import sys

LOG_FORMAT = "{asctime}: {levelname}: {name}: {funcName}(): {message}"
LOG_FORMATTER = logging.Formatter(LOG_FORMAT, style="{")
STDOUT_NAME = "stdout_stream_handler"


def _init_logger(name: str) -> logging.Logger:
    """Initialize logger with the default stdout stream handler

    Parameters
    ----------
    name : str
        Logger name

    Returns
    -------
    logging.Logger
        Logger Instance
    """
    # Logging setup
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Setup stream handler
    STREAM_HANDLER = logging.StreamHandler(sys.stdout)
    STREAM_HANDLER.setLevel(logging.INFO)
    STREAM_HANDLER.set_name(STDOUT_NAME)
    STREAM_HANDLER.setFormatter(LOG_FORMATTER)
    logger.addHandler(STREAM_HANDLER)
    return logger
