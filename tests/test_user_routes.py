import json
import os
from pathlib import Path
from urllib.parse import urlencode
from dateutil.parser import parse

import pytest
from async_asgi_testclient import TestClient
from odmantic.engine import AIOEngine

from natours.models.tour_model import Tour
from natours.models.user_model import User

pytestmark = pytest.mark.asyncio


async def test_sign_up(test_client: TestClient):
    body = {
            "username":"test",
            "password":"1234",
            "confirm_password":"1234",
            "email": "test@email.com"
            }
    response = await test_client.post("/api/v1/users/signup", json=body)
    response.json()["status"] == "success"
    response.status_code == 200


async def test_get_token(test_client: TestClient):
    param = {"username":"test", "password":"1234"}

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response =  await test_client.post("/api/v1/users/token", data=urlencode(param), headers=headers)
    assert response.status_code == 200



async def test_get_me(test_client: TestClient, admin_token_header: dict):
    response = await test_client.get("/api/v1/users/me", headers=admin_token_header)
    assert response.status_code == 200


# test forgot password

# test reset password

# test update my password

# test update me

# test deleteme


# test get all users

async def test_get_users(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    response = await test_client.get("/api/v1/users/", headers=admin_token_header)
    assert response.status_code == 200
    assert len(response.json()) == 2

# test get user by id


async def test_get_user(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
    user = await engine.find(User)
    user_id = user[0].dict()["id"]
    username = user[0].dict()["username"]
    response = await test_client.get(f"/api/v1/users/{user_id}", headers=admin_token_header)
    assert response.status_code == 200
    data = response.json()["user"]
    assert data["username"] == username
    

# test patch user


# async def test_patch_tour(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
#     tour = await engine.find(Tour)
#     tour_id = tour[0].dict()["id"]
#     tour_name = tour[0].dict()["name"]
#     response = await test_client.patch(
#         f"/api/v1/tours/{tour_id}", json=dict(name="this is the tour new name") , headers=admin_token_header
#     )
#     assert response.status_code == 200
#     tour = await engine.find(Tour, Tour.id == tour_id)
#     assert tour[0].dict()["name"] == "this is the tour new name"
#     assert tour[0].dict()["name"] != tour_name
#     response = await test_client.patch(
#         f"/api/v1/tours/{tour_id}", json=dict(name=tour_name), headers=admin_token_header
#     )
#     assert response.status_code == 200
#     tour = await engine.find(Tour, Tour.id == tour_id)
#     assert tour[0].dict()["name"] == tour_name


# test delete user by id

# async def test_delete_tour(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
#     tour = await engine.find(Tour)
#     tour_id = tour[0].dict()["id"]
#     response = await test_client.delete(f"/api/v1/tours/{tour_id}", headers=admin_token_header)
#     assert response.status_code == 200
#     assert await engine.find(Tour, Tour.id == tour_id) == []
#     tours = await engine.find(Tour)
#     assert len(tours) == 8

 

# async def test_post_tours(test_client: TestClient, engine: AIOEngine, admin_token_header: dict):
#     p = Path(os.path.dirname(__file__)).resolve().parent
#     with open(p / "natours/dev-data/data/tours.json", "r") as fp:
#         data = json.load(fp)
#     for tour in data:
#         response = await test_client.post("/api/v1/tours/", json=prep_tour(tour), headers=admin_token_header)
#         assert response.status_code == 200

#     fetched_from_db = await engine.find(Tour)
#     assert len(fetched_from_db) == 9


