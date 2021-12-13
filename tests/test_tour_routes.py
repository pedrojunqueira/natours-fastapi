import json
from pathlib import Path
from urllib.parse import urlencode
from dateutil.parser import parse

import pytest
from async_asgi_testclient import TestClient
from odmantic.engine import AIOEngine

from natours.models.tour_model import Tour

pytestmark = pytest.mark.asyncio


# test happy path

def prep_tour(tour:dict):
    tour["startDates"] = [ parse(d, ignoretz=True).isoformat() for d in tour["startDates"]]
    tour["id"] = tour["_id"]
    del tour["_id"]
    return tour


async def test_heart_beat(test_client: TestClient):
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"I ❤️ FastAPI": "🙋🏽‍♂️"}

 

async def test_post_tours(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    p = Path(__file__).parent.resolve().parent
    with open(p / "natours/dev-data/data/tours.json", "r") as fp:
        data = json.load(fp)
    for tour in data:
        response = await test_client.post("/api/v1/tours/", json=prep_tour(tour), headers=admin_token_header)
        assert response.status_code == 200

    fetched_from_db = await engine.find(Tour)
    assert len(fetched_from_db) == 9


async def test_get_tours(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    response = await test_client.get("/api/v1/tours/", headers=admin_token_header)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["results"] == 9
    assert await engine.find(Tour) is not None


async def test_get_tour(test_client: TestClient, engine: AIOEngine):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    tour_name = tour[0].dict()["name"]
    tour_difficulty = tour[0].dict()["difficulty"]
    response = await test_client.get(f"/api/v1/tours/{tour_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == tour_name
    assert data["difficulty"] == tour_difficulty


async def test_patch_tour(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    tour_name = tour[0].dict()["name"]
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id}", json=dict(name="this is the tour new name") , headers=admin_token_header
    )
    assert response.status_code == 200
    tour = await engine.find(Tour, Tour.id == tour_id)
    assert tour[0].dict()["name"] == "this is the tour new name"
    assert tour[0].dict()["name"] != tour_name
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id}", json=dict(name=tour_name), headers=admin_token_header
    )
    assert response.status_code == 200
    tour = await engine.find(Tour, Tour.id == tour_id)
    assert tour[0].dict()["name"] == tour_name


async def test_tour_stats(test_client: TestClient, engine: AIOEngine):
    response = await test_client.get("/api/v1/tours/tour-stats")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tour stats"]) == 3
    assert sum([stat["numTours"] for stat in data["tour stats"]]) == 7


@pytest.mark.parametrize("year, status_code", [(2021, 200), (99999, 404)])
async def test_monthly_plan(test_client: TestClient, year: int, status_code: int):
    response = await test_client.get(f"/api/v1/tours/monthly-plan/{year}")
    assert response.status_code == status_code
    data = response.json()


async def test_delete_tour(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    response = await test_client.delete(f"/api/v1/tours/{tour_id}", headers=admin_token_header)
    assert response.status_code == 200
    assert await engine.find(Tour, Tour.id == tour_id) == []
    tours = await engine.find(Tour)
    assert len(tours) == 8


# test errors and fails

async def test_inexistent_path(test_client: TestClient):
    response = await test_client.get(
        "/it-is-impossible-an-api-end-point-be-called-like-this"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


async def test_get_tour_non_existing_id_but_valid_object_id(
    test_client: TestClient, engine: AIOEngine
):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    tour_id_str = f"{tour_id}"
    response = await test_client.get(f"/api/v1/tours/{tour_id_str[:-8]}12345678")
    assert response.json() == {"detail": "could not find item"}


async def test_get_tour_with_invalid_object_id(
    test_client: TestClient, engine: AIOEngine
):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    tour_id_str = f"{tour_id}"
    response = await test_client.get(f"/api/v1/tours/{tour_id_str[:-1]}")
    data = response.json()
    assert data["detail"][0]["msg"] == "invalid ObjectId specified"


async def test_patch_tour_with_invalid_object_id(
    test_client: TestClient, engine: AIOEngine, admin_token_header: dict
):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    tour_id_str = f"{tour_id}"
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id_str[:-4]}4321",
        json=dict(name="this is the tour new name", duration=444) , headers=admin_token_header
    )
    assert response.status_code == 404
    response = await test_client.patch(
        f"/api/v1/tours/{tour_id_str[:-4]}",
        json=dict(name="this is the tour new name", duration=444) , headers=admin_token_header
    )
    assert response.status_code == 422


async def test_delete_tour_with_invalid_object_id(
    test_client: TestClient, engine: AIOEngine, admin_token_header: dict
):
    tour = await engine.find(Tour)
    tour_id = tour[0].dict()["id"]
    tour_id_str = f"{tour_id}"
    response = await test_client.delete(f"/api/v1/tours/{tour_id_str[:-4]}4321", headers=admin_token_header)
    assert response.status_code == 404
    response = await test_client.delete(f"/api/v1/tours/{tour_id_str[:-4]}", headers=admin_token_header)
    assert response.status_code == 422
