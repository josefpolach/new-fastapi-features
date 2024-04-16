import pytest

from app.dependencies import get_llm_provider
from app.main import app
from tests.mocks.mock_llm_provider import MockLLMProvider


@pytest.fixture
def mock_llm_provider_success() -> MockLLMProvider:
    return MockLLMProvider(behavior="succeed")


@pytest.fixture
def mock_llm_provider_none() -> MockLLMProvider:
    return MockLLMProvider(behavior="fail_with_none")


@pytest.fixture
def mock_llm_provider_llm_error() -> MockLLMProvider:
    return MockLLMProvider(behavior="fail_with_llm_error")


@pytest.fixture
def mock_llm_provider_exception() -> MockLLMProvider:
    return MockLLMProvider(behavior="fail_with_exception")


@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_pokemon_empty_description(async_client):
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": ""}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Pokemon description must not be empty"}


@pytest.mark.asyncio
async def test_pokemon_description_too_long(async_client):
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "." * 501}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Pokemon description must not exceed 500 characters"
    }


@pytest.mark.asyncio
async def test_pokemon_success_pikachu(async_client, mock_llm_provider_success):
    app.dependency_overrides[get_llm_provider] = lambda: mock_llm_provider_success
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "Pikachu"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 25,
        "name": "Pikachu",
        "height": 40,
        "weight": 6,
        "category": "Mouse",
        "types": ["Electric"],
        "weaknesses": ["Ground"],
        "ability": "Static",
        "stats": {
            "hp": 35,
            "attack": 55,
            "defense": 40,
            "special_attack": 50,
            "special_defense": 50,
            "speed": 90,
        },
    }
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_pokemon_internal_server_error(async_client, mock_llm_provider_exception):
    app.dependency_overrides[get_llm_provider] = lambda: mock_llm_provider_exception
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "Pikachu"}
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred: Unknown error"}
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_pokemon_llm_error(async_client, mock_llm_provider_llm_error):
    app.dependency_overrides[get_llm_provider] = lambda: mock_llm_provider_llm_error
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "Pikachu"}
    )
    assert response.status_code == 502
    assert response.json() == {
        "detail": "An error occurred on the side of the LLM Provider"
    }
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_pokemon_unidentified(async_client, mock_llm_provider_none):
    app.dependency_overrides[get_llm_provider] = lambda: mock_llm_provider_none
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "Unknown creature"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Could not identify a pokemon from the description"
    }
    app.dependency_overrides.clear()
