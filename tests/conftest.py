import asyncio
from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from mard.app import app
from mard.config import settings
from mard.database import get_session
from mard.models import table_registry

test_engine = create_async_engine(
    settings.test_database_url,
    poolclass=NullPool,
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='session', autouse=True)
def _prepare_database() -> Iterator[None]:
    async def create_schema() -> None:
        async with test_engine.begin() as connection:
            await connection.run_sync(table_registry.metadata.create_all)

    async def drop_schema() -> None:
        async with test_engine.begin() as connection:
            await connection.run_sync(table_registry.metadata.drop_all)
        await test_engine.dispose()

    asyncio.run(create_schema())
    yield
    asyncio.run(drop_schema())


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session
