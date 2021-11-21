from unittest.mock import patch
from pathlib import Path
import json
import os
from datetime import datetime

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

# test happy path

async def test_heart_beat(test_client: TestClient):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"I ❤️ FastAPI": "🙋🏽‍♂️"}


async def test_post_tours(test_client: TestClient, engine: AIOEngine):
    p = Path(os.path.dirname(__file__)).resolve().parent
    with open(p / "natours/dev-data/data/tours-simple.json", "r") as fp:
        data = json.load(fp)
    tours = [{k: v for k, v in d.items() if k != "id"} for d in data]
    for tour in tours:
        tour["startDates"] = [
            datetime.strptime(d, "%Y-%m-%d,%H:%M").isoformat()
            for d in tour["startDates"]
        ]
        response = await test_client.post("/api/v1/tours/", json=tour)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    fetched_from_db = await engine.find(Tours)
    assert len(fetched_from_db) == 9


async def test_get_tours(test_client: TestClient, engine: AIOEngine):
    response = await test_client.get("/api/v1/tours/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["results"] == 9
    assert await engine.find(Tours) is not None


async def test_get_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    tour_name = tour[0].dict()["name"]
    tour_difficulty = tour[0].dict()["difficulty"]
    response = await test_client.get(f"/api/v1/tours/{tour_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == tour_name
    assert data["difficulty"] == tour_difficulty


async def test_patch_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    tour_name = tour[0].dict()["name"]
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id}", json=dict(name="this is the tour new name")
    )
    assert response.status_code == 200
    tour = await engine.find(Tours, Tours.id == tour_id)
    assert tour[0].dict()["name"] == "this is the tour new name"
    assert tour[0].dict()["name"] != tour_name
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id}", json=dict(name=tour_name)
    )
    assert response.status_code == 200
    tour = await engine.find(Tours, Tours.id == tour_id)
    assert tour[0].dict()["name"] == tour_name


async def test_tour_stats(test_client: TestClient, engine: AIOEngine):
    response = await test_client.get("/api/v1/tours/tour-stats")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tour stats"]) == 3
    assert sum([stat["numTours"] for stat in data["tour stats"]]) == 9


async def test_monthly_plan(test_client: TestClient, engine: AIOEngine):
    year = 2021
    response = await test_client.get(f"/api/v1/tours/monthly-plan/{year}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data[f"year plan for {year}"], list)
    
async def test_delete_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    response = await test_client.delete(f"/api/v1/tours/{tour_id}")
    assert response.status_code == 200
    assert await engine.find(Tours, Tours.id == tour_id) == []
    tours = await engine.find(Tours)
    assert len(tours) == 8

# test errors and fails

async def test_inexistent_path(test_client: TestClient):
    response = await test_client.get("/it-is-impossible-an-api-end-point-be-called-like-this")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

async def test_get_tour_non_existing_id_but_valid_object_id(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    tour_id_str = f"{tour_id}"
    response = await test_client.get(f"/api/v1/tours/{tour_id_str[:-8]}12345678")
    assert response.json() == {'detail': 'could not find item'}
    
async def test_get_tour_with_invalid_object_id(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tours)
    tour_id = tour[0].dict()["id"]
    tour_id_str = f"{tour_id}"
    response = await test_client.get(f"/api/v1/tours/{tour_id_str[:-1]}")
    data = response.json()
    assert data['detail'][0]["msg"] ==  'invalid ObjectId specified'
    
