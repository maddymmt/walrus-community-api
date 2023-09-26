import datetime
from typing import List, TypedDict

from pydantic import BaseModel, Field


class Walrus(BaseModel):
    name: str
    friends: List[str] = Field(default_factory=list)
    favourite_food: str
    birth_date: datetime.date


class WalrusDict(TypedDict):
    name: str
    friends: List[str]
    favourite_food: str
    birth_date: datetime.date
