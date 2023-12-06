import os
import asyncio
from loguru import logger
from fitness_api import settings as _settings

def check_logging_level() -> None:
    """
    checks the logging level based on the IOT_API_DEBUG_LOGGING environment variable
    """
    # Define logging level
    logger.remove()
    if _settings.SETTINGS.debug_logging:
        logger.add(os.sys.stderr, level="DEBUG", backtrace=True, diagnose=True)
        logger.info(f"LOGURU_LEVEL: {'DEBUG'}")
    else:
        logger.add(os.sys.stderr, level="INFO")
        logger.info(f"LOGURU_LEVEL: {'INFO'}")
