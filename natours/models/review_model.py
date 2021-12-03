from datetime import datetime

from odmantic import Field, Model, ObjectId


class Review(Model):
    review:str
    rating:int = Field(gt=0, lt=6)
    user:ObjectId
    tour:ObjectId
    createdAt: datetime = Field(default=datetime.now())
    
    class Config:
        collection = "reviews"
