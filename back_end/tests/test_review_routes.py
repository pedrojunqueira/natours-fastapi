import json
from pathlib import Path

import pytest
from async_asgi_testclient import TestClient, response
from odmantic.engine import AIOEngine
from dateutil.parser import parse

from natours.models.tour_model import Tour

from natours.models.review_model import Review

pytestmark = pytest.mark.asyncio

def prep_tour(tour:dict):
    tour["startDates"] = [ parse(d, ignoretz=True).isoformat() for d in tour["startDates"]]
    tour["id"] = tour["_id"]
    del tour["_id"]
    return tour


async def test_post_one_tour(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    p = Path(__file__).parent.resolve().parent
    with open(p / "natours/dev-data/data/tours.json", "r") as fp:
        data = json.load(fp)
    
    tour = data[0]

    response = await test_client.post("/api/v1/tours/", json=prep_tour(tour), headers=admin_token_header)
    assert response.status_code == 200


async def test_post_tour_review(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    tours = await engine.find(Tour)
    tour_id = tours[0].id
    review = {
            "review": "This is my test review about the tour",
            "rating": 4
            }
    response = await test_client.post(f"/api/v1/tours/{tour_id}/reviews", headers=admin_token_header , json=review)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["review added"]["review"] == review["review"]


async def test_get_tour_review(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    tours = await engine.find(Tour)
    tour_id = tours[0].id
    response = await test_client.get(f"/api/v1/tours/{tour_id}/reviews", headers=admin_token_header)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_get_reviews(test_client: TestClient):
    response = await test_client.get("/api/v1/reviews/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_get_review_by_id(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    reviews = await engine.find(Review)
    review_id = reviews[0].id
    response = await test_client.get(f"/api/v1/reviews/{review_id}", headers=admin_token_header)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_delete_review(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    reviews = await engine.find(Review)
    review_id = reviews[0].id
    response = await test_client.delete(f"/api/v1/reviews/{review_id}", headers=admin_token_header)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    reviews = await engine.find(Review)
    assert not reviews

    
    

