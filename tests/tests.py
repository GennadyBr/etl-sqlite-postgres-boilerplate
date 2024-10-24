""" Test """
import pytest

from src.core.logger import logger


@pytest.mark.asyncio()
async def test_hello() -> None:
    """Test hello world"""
    logger.info('Test hello world')
