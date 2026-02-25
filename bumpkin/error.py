import logging

logger = logging.getLogger("bumpkin.error")


def report_error(exception, context=None, level=logging.ERROR):
    """
    Centralized error reporting function.
    Logs the error and context using the standard logger.
    If Sentry is configured (future), it would report there.
    """
    msg = f"Unexpected error: {exception}"
    if context:
        msg += f" | Context: {context}"

    logger.log(level, msg, exc_info=True)
