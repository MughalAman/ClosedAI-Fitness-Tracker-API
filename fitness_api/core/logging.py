import os
from fitness_api import settings as _settings
from loguru import logger

def setup_logging():
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
setup_logging()

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
