from pydantic import BaseModel
from typing import List
from datetime import date
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class NewLocation(BaseModel):
    sector: str
    description: str
    photo1: str
    photo2: Optional[str]
    #registration_date: date.today()

class Location(BaseModel):
    id_location: int
    sector: str
    description: str
    photos: List[str] = []
    still_there: int = 0
    not_still_there: int = 0
    comments: List[str] = []

class Comment(BaseModel):
    text: str

class LocationsList(BaseModel):
    id_location: int
    sector: str
    username: str
    resgitration_date: date
