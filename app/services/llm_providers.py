import logging
from abc import ABC, abstractmethod

import instructor
from openai import APIError, AsyncOpenAI

from app.schemas.pokemon import MaybePokemon


class LLMProviderError(Exception):
    def __init__(self, message="LLM provider error occurred"):
        self.message = message
        super().__init__(self.message)


class LLMProvider(ABC):
    @abstractmethod
    async def identify_pokemon(self, query: str) -> MaybePokemon:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = instructor.from_openai(AsyncOpenAI(api_key=api_key))
        self.logger = logging.getLogger(f"app.{self.__class__.__name__}")

    async def identify_pokemon(self, pokemon_description: str) -> MaybePokemon:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"What are the stats of the following pokemon? Pokemon name or description: {pokemon_description}. Respond with the provided schema.",
                    },
                ],
                response_model=MaybePokemon,
            )
        except APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise LLMProviderError(f"OpenAI API error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

        return response
