import pytest
from httpx import ASGITransport, AsyncClient

from pixelfuse.config import Settings
from pixelfuse.main import create_app


@pytest.fixture
def settings() -> Settings:
    return Settings(allowed_origins=["*"])


@pytest.fixture
async def client(settings: Settings) -> AsyncClient:
    app = create_app(settings)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac  # type: ignore[misc]
