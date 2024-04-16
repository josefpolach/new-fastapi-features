from typing import List, Optional

from pydantic import BaseModel, Field


class Stats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class Pokemon(BaseModel):
    id: int
    name: str
    height: float = Field(..., description="Height of the pokemon in cm")
    weight: float = Field(..., description="Weight of the pokemon in kg")
    category: str
    types: List[str]
    weaknesses: List[str]
    ability: str
    stats: Stats = Field(..., description="Base stats of th pokemon")


class MaybePokemon(BaseModel):
    pokemon: Optional[Pokemon] = Field(
        default=None, description="Information about the identified pokemon or None"
    )
    identified: bool = Field(
        default=False, description="Indicates whether a pokemon was identified"
    )

    def __bool__(self):
        return self.identified and self.pokemon is not None
