from datetime import datetime
from typing import List, Optional

from odmantic import Field, Model


class Tours(Model):
    name: str
    duration: float
    maxGroupSize: int
    difficulty: str
    ratingsAverage: Optional[float] = Field(default=4.5)
    ratingsQuantity: Optional[int]
    price: float
    summary: str
    description: Optional[str]
    imageCover: str
    images: List[str]
    startDates: List[datetime]
    createdAt: datetime = Field(default=datetime.now())

    class Config:
        schema_extra = {
            "example": {
                "name": "The Forest Hiker",
                "duration": 5,
                "maxGroupSize": 25,
                "difficulty": "easy",
                "ratingsAverage": 4.7,
                "ratingsQuantity": 37,
                "price": 397,
                "summary": "Breathtaking hike through the Canadian Banff National Park",
                "description": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                "imageCover": "tour-1-cover.jpg",
                "images": ["tour-1-1.jpg", "tour-1-2.jpg", "tour-1-3.jpg"],
                "startDates": [
                    "2021-04-25T10:00:00",
                    "2021-07-20T10:00:00",
                    "2021-10-05T10:00:00",
                ],
            }
        }
