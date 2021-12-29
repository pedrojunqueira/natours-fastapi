from datetime import datetime
from typing import Optional

from odmantic import Field, Model, ObjectId


class Review(Model):
    review: str
    rating: int = Field(gt=0, lt=6)
    user: Optional[ObjectId]
    tour: Optional[ObjectId]
    createdAt: datetime = Field(default=datetime.now())

    class Config:
        collection = "reviews"
