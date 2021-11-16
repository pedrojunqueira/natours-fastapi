from odmantic import Model


class Tours(Model):
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
