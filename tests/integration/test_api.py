import pytest


@pytest.fixture
def successful_response() -> dict:
    return {
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


@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_pokemon_success_name_exact(async_client, successful_response):
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "Pikachu"}
    )
    assert response.status_code == 200
    assert response.json() == successful_response


@pytest.mark.asyncio
async def test_pokemon_success_name_approximate(async_client, successful_response):
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "picacu"}
    )
    assert response.status_code == 200
    assert response.json() == successful_response


@pytest.mark.asyncio
async def test_pokemon_success_description(async_client, successful_response):
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "the famous yellow one"}
    )
    assert response.status_code == 200
    assert response.json() == successful_response


@pytest.mark.asyncio
async def test_pokemon_not_identified(async_client):
    response = await async_client.post(
        "/pokemon/identify", json={"pokemon_description": "Andrej Babiš"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Could not identify a pokemon from the description"
    }
