from pydantic import BaseModel


class Query(BaseModel):
    pokemon_description: str
