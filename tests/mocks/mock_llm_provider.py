from app.schemas.pokemon import MaybePokemon, Pokemon, Stats
from app.services.llm_providers import LLMProvider, LLMProviderError


class MockLLMProvider(LLMProvider):
    def __init__(self, behavior="succeed"):
        self.behavior = behavior

    async def identify_pokemon(self, query: str) -> MaybePokemon:
        match self.behavior:
            case "succeed":
                match query:
                    case "Pikachu":
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
                    case _:
                        raise ValueError("Unsupported query")
            case "fail_with_none":
                return MaybePokemon(identified=False, pokemon=None)
            case "fail_with_llm_error":
                raise LLMProviderError("An error occurred")
            case "fail_with_exception":
                raise Exception("Unknown error")
            case _:
                raise ValueError("Unsupported behavior")
