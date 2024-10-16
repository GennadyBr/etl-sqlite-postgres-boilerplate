""" Test """
import pytest
from httpx import ASGITransport, AsyncClient

from src.core.logger import logger
from src.main import app


@pytest.mark.asyncio()
async def test_hello() -> None:
    """Test hello world"""
    logger.info('Test hello world')
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url='http://test',
    ) as client:
        response = await client.get('/hello')
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_request() -> None:
    """Test request example"""
    logger.info('Test request example')
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url='http://test',
    ) as client:
        response = await client.get('/request')
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_raise_error() -> None:
    """Test raise error"""
    logger.info('Test raise error')
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url='http://test',
    ) as client:
        response = await client.get('/raise_error')
        assert response.status_code == 200
