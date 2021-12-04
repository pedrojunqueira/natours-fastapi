from datetime import datetime
from typing import List, Optional

from odmantic import Field, Model, EmbeddedModel, ObjectId
from pydantic import BaseModel

class StartLocation(BaseModel):
    description: str
    type: str
    coordinates: List[float]
    address: str

class Location(EmbeddedModel):
    description: str
    type: str
    coordinates: List[float]
    day: int

class Tour(Model):
    name: str
    duration: int
    maxGroupSize: int
    difficulty: str
    ratingsAverage: Optional[float] = Field(default=4.5)
    ratingsQuantity: Optional[int]
    price: float
    summary: str
    description: Optional[str]
    imageCover: str
    images: List[str]
    startDates: Optional[List[datetime]]
    createdAt: datetime = Field(default=datetime.now())
    startLocation: Optional[StartLocation]
    imageCover: str
    guides: Optional[List[ObjectId]]
    locations: Optional[List[Location]]
    class Config:
        collection = "tours"


