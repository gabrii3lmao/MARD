import asyncio
import os
from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from testcontainers.community.postgres import PostgresContainer

from mard.app import app
from mard.database import get_session
from mard.models import User, table_registry

os.environ.setdefault('TESTCONTAINERS_RYUK_DISABLED', 'true')


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer(
        'postgres:17-alpine',
        driver='asyncpg',
        username='mard',
        password='mard',
        dbname='mard_test',
    ) as container:
        _engine = create_async_engine(
            container.get_connection_url(),
            poolclass=NullPool,
        )
        yield _engine
        asyncio.run(_engine.dispose())


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with engine.begin() as connection:
        await connection.run_sync(table_registry.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as db_session:
        yield db_session
        await db_session.rollback()

    async with engine.begin() as connection:
        await connection.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    async def override_get_session() -> AsyncIterator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url='http://test'
    ) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(session: AsyncSession) -> User:
    user_db = User(
        username='lucas',
        email='lucas@email.com',
        password='123456',
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    user_db.clean_password = user_db.password
    return user_db
