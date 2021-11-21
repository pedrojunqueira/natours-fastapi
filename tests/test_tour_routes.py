from unittest.mock import patch
from pydantic.types import Json

import pytest
from async_asgi_testclient import TestClient

from odmantic.engine import AIOEngine
from natours.models.tour_model import Tours

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def test_client(engine: AIOEngine) -> TestClient:
    with patch("natours.models.database.engine", engine):
        from natours.app import app

        async with TestClient(app) as client:
            yield client


new_tour = {
    "name": "The test newtour",
    "duration": 10,
    "maxGroupSize": 44,
    "difficulty": "medium",
    "ratingsAverage": 4.5,
    "ratingsQuantity": 42,
    "price": 399,
    "summary": "Breathtaking hike through the Tiger Chinese Part",
    "description": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit or incididunt ut labore et dolore magna aliqua. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "imageCover": "tour-1-cover.jpg",
    "images": ["tour-1-1.jpg", "tour-1-2.jpg", "tour-1-3.jpg"],
    "startDates": ["2021-04-25T10:00:00", "2021-07-20T10:00:00", "2022-10-05T10:00:00"],
}


async def test_heart_beat(test_client: TestClient):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"I ❤️ FastAPI": "🙋🏽‍♂️"}


async def test_post_tour(test_client: TestClient, engine: AIOEngine):
    response = await test_client.post("/api/v1/tours/", json=new_tour)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


async def test_get_tours(test_client: TestClient, engine: AIOEngine):
    response = await test_client.get("/api/v1/tours/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["results"] == 1
    assert await engine.find(Tours) is not None


async def test_get_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    response = await test_client.get(f"/api/v1/tours/{tour_id}")
    assert response.status_code == 200
    for key, value in new_tour.items():
        r = response.json()["data"]
        assert r[key] == value


async def test_patch_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id}", json=dict(name="this is the tour new name")
    )
    assert response.status_code == 200
    tour = await engine.find(Tours, Tours.id == tour_id)
    assert tour[0].dict()["name"] == "this is the tour new name"


async def test_tour_stats(test_client: TestClient, engine: AIOEngine):
    response = await test_client.get("/api/v1/tours/tour-stats")
    assert response.status_code == 200
    assert response.json() == {
        "tour stats": [
            {
                "_id": "MEDIUM",
                "numTours": 1,
                "numRatings": 42,
                "avgRating": 4.5,
                "avgPrice": 399.0,
                "minPrice": 399.0,
                "maxPrice": 399.0,
            }
        ]
    }


async def test_tour_stats(test_client: TestClient, engine: AIOEngine):
    year = 2021
    response = await test_client.get(f"/api/v1/tours/monthly-plan/{year}")
    assert response.status_code == 200
    assert response.json() == {
        "year plan for 2021": [
            {"numTourStarts": 1, "tours": ["this is the tour new name"], "month": 7},
            {"numTourStarts": 1, "tours": ["this is the tour new name"], "month": 4},
        ]
    }


async def test_delete_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    response = await test_client.delete(f"/api/v1/tours/{tour_id}")
    assert response.status_code == 200
    assert await engine.find(Tours, Tours.id == tour_id) == []
