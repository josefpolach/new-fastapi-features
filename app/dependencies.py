from app.config import settings
from app.services.llm_providers import LLMProvider, OpenAIProvider


async def get_llm_provider() -> LLMProvider:
    match settings.llm_provider:
        case "openai":
            return OpenAIProvider(api_key=settings.openai_api_key)
        case _:
            raise ValueError(f"Invalid LLM provider: {settings.llm_provider}")
