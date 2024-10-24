""" Test """
import pytest
from httpx import ASGITransport, AsyncClient

from src.core.logger import logger
from src.main import app
from src.schemas.schemas_tables import UsersTable

table = UsersTable(
    schema_name='content',
    table_name='test_table',
)
item_id: str


@pytest.mark.asyncio()
async def test_sqlite_get_all_table_names() -> None:
    """Test /sqlite/get_all_table_names"""
    url = '/sqlite/get_all_table_names'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.get(url)
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_sqlite_get_batch_records() -> None:
    """Test /sqlite/get_batch_records"""
    url = '/sqlite/get_batch_records'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.get(url)
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_sqlite_get_row_number_by_table() -> None:
    """Test /sqlite/get_row_number_by_table"""
    url = '/sqlite/get_row_number_by_table'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.get(url)
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_create_table() -> None:
    """ Test /postgres/create_table"""
    url = '/postgres/create_table'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_get_row_number_by_table() -> None:
    """ Test /postgres/get_row_number_by_table"""
    url = '/postgres/get_row_number_by_table'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_get_all_table_names() -> None:
    """Test /postgres/get_all_table_names"""
    url = '/postgres/get_all_table_names'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_get_all_records() -> None:
    """Test /postgres/get_all_records"""
    url = '/postgres/get_all_records'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_insert_one() -> None:
    """ Test /postgres/insert_one"""
    url = '/postgres/insert_one'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        global item_id
        item_id = response.json()[0]
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_get_by_id() -> None:
    """ Test /postgres/get_by_id """
    url = '/postgres/get_by_id'
    global item_id
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(
            url + '?item_id=' + item_id, json=table.dict(),
        )
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_insert_many() -> None:
    """ Test /postgres/insert_many"""
    url = '/postgres/insert_many'
    params: dict = {}
    params['params'] = table.dict()
    params['names'] = ['test1', 'test2', 'test3']
    logger.info(params)
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=params)
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_truncate_table() -> None:
    """Test /postgres/truncate_table"""
    url = '/postgres/truncate_table'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_trancate_all_tables() -> None:
    """Test /postgres/truncate_all_tables"""
    url = '/postgres/truncate_all_tables'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_postgres_drop_table() -> None:
    """Test /postgres/drop_table"""
    url = '/postgres/drop_table'
    async with AsyncClient(
            base_url='http://test',
            transport=ASGITransport(app=app),
    ) as client:
        response = await client.post(url, json=table.dict())
        assert response.status_code == 200
