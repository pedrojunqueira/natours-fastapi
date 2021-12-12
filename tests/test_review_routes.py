import pytest
from async_asgi_testclient import TestClient
from odmantic.engine import AIOEngine
from dateutil.parser import parse

from natours.models.tour_model import Tour

pytestmark = pytest.mark.asyncio

def prep_tour(tour:dict):
    tour["startDates"] = [ parse(d, ignoretz=True).isoformat() for d in tour["startDates"]]
    tour["id"] = tour["_id"]
    del tour["_id"]
    return tour

# populate db with 1 tour

tour = {
    "startLocation": {
      "description": "Miami, USA",
      "type": "Point",
      "coordinates": [-80.185942, 25.774772],
      "address": "301 Biscayne Blvd, Miami, FL 33132, USA"
    },
    "ratingsAverage": 4.8,
    "ratingsQuantity": 6,
    "images": ["tour-2-1.jpg", "tour-2-2.jpg", "tour-2-3.jpg"],
    "startDates": [
      "2021-06-19T09:00:00.000Z",
      "2021-07-20T09:00:00.000Z",
      "2021-08-18T09:00:00.000Z"
    ],
    "_id": "5c88fa8cf4afda39709c2955",
    "name": "The Sea Explorer",
    "duration": 7,
    "maxGroupSize": 15,
    "difficulty": "medium",
    "guides": ["5c8a22c62f8fb814b56fa18b", "5c8a1f4e2f8fb814b56fa185"],
    "price": 497,
    "summary": "Exploring the jaw-dropping US east coast by foot and by boat",
    "description": "Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\nIrure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    "imageCover": "tour-2-cover.jpg",
    "locations": [
      {
        "_id": "5c88fa8cf4afda39709c2959",
        "description": "Lummus Park Beach",
        "type": "Point",
        "coordinates": [-80.128473, 25.781842],
        "day": 1
      },
      {
        "_id": "5c88fa8cf4afda39709c2958",
        "description": "Islamorada",
        "type": "Point",
        "coordinates": [-80.647885, 24.909047],
        "day": 2
      },
      {
        "_id": "5c88fa8cf4afda39709c2957",
        "description": "Sombrero Beach",
        "type": "Point",
        "coordinates": [-81.0784, 24.707496],
        "day": 3
      },
      {
        "_id": "5c88fa8cf4afda39709c2956",
        "description": "West Key",
        "type": "Point",
        "coordinates": [-81.768719, 24.552242],
        "day": 5
      }
    ]
  }

async def test_post_tours(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    
    response = await test_client.post("/api/v1/tours/", json=prep_tour(tour), headers=admin_token_header)
    assert response.status_code == 200


# test post tour review

async def test_post_tour_review(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    tours = await engine.find(Tour)
    tour_id = tours[0].id
    review = {
            "review": "This is my test review about the tour",
            "rating": 4
            }
    print(tour_id)
    response = await test_client.post(f"/api/v1/tours/{tour_id}/reviews", headers=admin_token_header , data=review)
    print(response.json())

# test get tour review (nested)

async def test_get_tour_review(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    pass


# test get reviews

async def test_get_reviews(test_client: TestClient):
    response = await test_client.get("/api/v1/reviews/")
    assert response.status_code == 200
    print(response.json())


# test get review by id

async def test_get_review_by_id():
    pass

# test delete review

async def test_delete_review():
    pass

