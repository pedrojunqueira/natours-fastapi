from datetime import datetime
from typing import List, Optional
from pathlib import Path
import json
import asyncio

from odmantic import Field, Model, EmbeddedModel, ObjectId, AIOEngine
from pydantic import BaseModel, EmailStr, validator
from dateutil.parser import parse
from motor.motor_asyncio import AsyncIOMotorClient


class Review(Model):
    review:str
    rating:int = Field(gt=0, lt=6)
    user:ObjectId
    tour:ObjectId
    createdAt: datetime = Field(default=datetime.now())
    
    class Config:
        collection = "reviews"

p = Path(__file__).parent.resolve()

with open(p / "dev-data" / "data" / "reviews.json", "r") as fp:
    revs = json.load(fp)

def prep_data(rv):
    rv["id"] = rv["_id"]
    del rv["_id"]
    return Review(**rv)


reviews =  [prep_data(r) for r in revs]


class User(Model):
    username: str
    email: EmailStr
    name: Optional[str]
    lastname: Optional[str]
    role: str
    active: Optional[bool]
    photo: Optional[str]
    password: str
    confirm_password: Optional[str]
    password_changed_at: Optional[datetime]
    password_reset_token: Optional[str]
    password_reset_expire: Optional[datetime]
    createdAt: datetime = Field(default=datetime.now())

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    class Config:
        collection = "users"

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


def prep_tour(tour:dict) -> Tour:
    tour["startDates"] = [ parse(d, ignoretz=True) for d in tour["startDates"]]
    tour["id"] = tour["_id"]
    del tour["_id"]
    return Tour(**tour)

p = Path(__file__).parent.resolve()

with open(p / "dev-data" / "data" / "tours.json", "r") as fp:
    trs = json.load(fp)


def name_to_username(name:str):
  return "".join(name.split(" ")).lower()

p = Path(__file__).parent.resolve()

with open(p / "dev-data" / "data" / "users.json", "r") as fp:
    usr = json.load(fp)

users = []
for u in usr:
  u["confirm_password"] =u["password"]
  u["username"] = name_to_username(u["name"])
  u["id"] = u["_id"]
  del u["_id"]
  u_ = User(**u)
  users.append(u_)
  
  
client = AsyncIOMotorClient("mongodb://localhost:27017/test")
engine = AIOEngine(motor_client=client, database="test")


print("loading db...")

loop = asyncio.get_event_loop()
loop.run_until_complete(engine.save_all([prep_tour(t) for t in trs]))
loop.run_until_complete(engine.save_all(users))
loop.run_until_complete(engine.save_all(reviews))
loop.close()

