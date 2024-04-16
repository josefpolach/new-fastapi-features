import os

import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(base_url=os.environ.get("API_URL")) as client:
        yield client
