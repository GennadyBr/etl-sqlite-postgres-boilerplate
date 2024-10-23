""" Test """
import pytest
from httpx import ASGITransport, AsyncClient

from src.core.logger import logger
from src.main import app


@pytest.mark.asyncio()
async def test_hello() -> None:
    """Test hello world"""
    logger.info('Test hello world')
