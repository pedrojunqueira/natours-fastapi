import mongoengine
from pydantic import BaseModel

class Tour(mongoengine.Document):
    name = mongoengine.StringField()
    rating = mongoengine.DecimalField()
    price = mongoengine.DecimalField()

    meta = {
        "collection": "tours",
    }

class TourSchema(BaseModel):
    name: str
    rating: float
    price: float
    class Config:
        schema_extra = {
            "example": {
                "name": "Forest Hiker",
                "rating": 2,
                "price": 400.3,
            }
        }



