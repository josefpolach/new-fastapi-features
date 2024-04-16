from unittest.mock import AsyncMock

import pytest
from openai import APIError

from app.schemas.pokemon import MaybePokemon, Pokemon, Stats
from app.services.llm_providers import LLMProviderError, OpenAIProvider


@pytest.fixture
def successful_response() -> MaybePokemon:
    return MaybePokemon(
        identified=True,
        pokemon=Pokemon(
            id=25,
            name="Pikachu",
            height=40,
            weight=6,
            category="Mouse",
            types=["Electric"],
            weaknesses=["Ground"],
            ability="Static",
            stats=Stats(
                hp=35,
                attack=55,
                defense=40,
                special_attack=50,
                special_defense=50,
                speed=90,
            ),
        ),
    )


@pytest.mark.asyncio
async def test_openai_provider_success(successful_response):
    provider = OpenAIProvider(api_key="mock_key")
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = successful_response
    provider.client = mock_client

    response = await provider.identify_pokemon("Pikachu")

    assert response == successful_response
    mock_client.chat.completions.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_openai_provider_api_error():
    provider = OpenAIProvider(api_key="mock_key")
    mock_client = AsyncMock()
    mock_client.chat.completions.create.side_effect = APIError(
        message="Some error", request=None, body=None
    )
    provider.client = mock_client

    with pytest.raises(LLMProviderError) as e_info:
        await provider.identify_pokemon("Pikachu")
    assert "OpenAI API error occurred" in str(e_info.value)
    mock_client.chat.completions.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_openai_provider_unexpected_error():
    provider = OpenAIProvider(api_key="mock_key")
    mock_client = AsyncMock()
    mock_client.chat.completions.create.side_effect = Exception("Some unexpected error")
    provider.client = mock_client

    with pytest.raises(Exception) as e_info:
        await provider.identify_pokemon("Pikachu")
    assert "An unexpected error occurred" in str(e_info.value)
    mock_client.chat.completions.create.assert_awaited_once()
