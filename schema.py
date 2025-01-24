from enum import Enum
from datetime import date
from pydantic import BaseModel, validator

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'
    ELECTRONIC = 'electronic'
    HIP_HOP = 'hip-hop'
    METAL = 'metal'

class GenreChoices(Enum):
    ROCK = 'Rock'
    POP = 'Pop'
    ELECTRONIC = 'Electronic'
    HIP_HOP = 'Hip-Hop'
    METAL = 'Metal'

class Album(BaseModel):
    title: str
    release_date: date

class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []

class BandCreate(BandBase):
    @validator('genre', pre=True)
    def title_case_genre(cls, v):
        return v.title()

class BandWithID(BandBase):
    id: int