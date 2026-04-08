import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.pg import engine, PgModel
from src.main import app
from src.config import get_pg_url

TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def db_session():
    # Create tables before test
    async with engine.begin() as conn:
        await conn.run_sync(PgModel.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    # Clean up tables after test
    async with engine.begin() as conn:
        await conn.run_sync(PgModel.metadata.drop_all)


@pytest.fixture(autouse=True)
async def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_pg_url] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
