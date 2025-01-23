from enum import Enum
from pydantic import BaseModel
from datetime import date

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'
    ELECTRONIC = 'electronic'
    HIP_HOP = 'hip-hop'
    METAL = 'metal'

class Album(BaseModel):
    title: str
    release_date: date

class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Album] = []

