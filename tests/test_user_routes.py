from datetime import datetime
from urllib.parse import urlencode
import base64

import pytest
from async_asgi_testclient import TestClient
from odmantic.engine import AIOEngine

from natours.models.user_model import User
from natours.controllers.email_controller import email_client

pytestmark = pytest.mark.asyncio


async def test_sign_up(test_client: TestClient):
    body = {
        "username": "test",
        "password": "1234",
        "confirm_password": "1234",
        "email": "test@email.com",
    }
    response = await test_client.post("/api/v1/users/signup", json=body)
    response.json()["status"] == "success"
    response.status_code == 200


@pytest.fixture()
async def test_token_header(test_client: TestClient):
    body = {
        "username": "test2",
        "password": "secret",
        "confirm_password": "secret",
        "email": "test2@email.com",
    }
    response = await test_client.post("/api/v1/users/signup", json=body)
    param = {"username": "test2", "password": "secret"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await test_client.post(
        "/api/v1/users/token", data=urlencode(param), headers=headers
    )
    token = response.json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}
    return h


async def test_get_token(test_client: TestClient):
    param = {"username": "test", "password": "1234"}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await test_client.post(
        "/api/v1/users/token", data=urlencode(param), headers=headers
    )
    assert response.status_code == 200


async def test_get_me(test_client: TestClient, admin_token_header: dict):
    response = await test_client.get("/api/v1/users/me", headers=admin_token_header)
    assert response.status_code == 200


# @pytest.mark.skip
async def test_forgot_password(test_client: TestClient, engine: AIOEngine):
    payload = {"email": "test@email.com"}
    response = await test_client.post("/api/v1/users/forgotpassword", json=payload)
    response.json()["status"] == "success"
    assert response.status_code == 200
    user = await engine.find_one(User, User.email == "test@email.com")
    assert user.password_reset_token is not None
    assert round((user.password_reset_expire - datetime.now()).seconds / 60) == 20


def decoder(string):
    decoded = base64.b64decode(string)
    return decoded.decode()


# @pytest.mark.skip
async def test_reset_password_with_token(test_client: TestClient):
    email_client.config.SUPPRESS_SEND = 1
    with email_client.record_messages() as outbox:
        payload = {"email": "test@email.com"}
        response = await test_client.post("/api/v1/users/forgotpassword", json=payload)
        assert response.status_code == 200
        assert len(outbox) == 1
        assert outbox[0]["To"] == "test@email.com"
        string = (outbox[0].get_payload()[0]).as_string()
        message = "".join(string.split()[-3:])
        token = decoder(message).split()[-2].split("/")[-1]
        payload = {"password": "newpass", "confirm_password": "newpass"}
        response = await test_client.patch(
            f"/api/v1/users/resetpassword/{token}", json=payload
        )
        assert response.status_code == 200


async def test_update_me(
    test_client: TestClient, test_token_header: dict, engine: AIOEngine
):
    user = await engine.find_one(User, User.email == "test2@email.com")
    assert user.name == None
    assert user.lastname == None
    body = {
        "name": "test_name",
        "lastname": "test_lastname",
    }
    response = await test_client.patch(
        "/api/v1/users/updateme", headers=test_token_header, json=body
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    user = await engine.find_one(User, User.email == "test2@email.com")
    assert user.name == body["name"]
    assert user.lastname == body["lastname"]


async def test_update_my_password(test_client: TestClient, test_token_header: dict):
    body = {
        "current_password": "secret",
        "password": "newsecret",
        "confirm_password": "newsecret",
    }
    response = await test_client.patch(
        "/api/v1/users/updatemypassword", headers=test_token_header, json=body
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert (
        response.json()["message"]
        == "password successfully updated for test2@email.com"
    )


async def test_delete_me(test_client: TestClient, engine: AIOEngine):
    param = {"username": "test2", "password": "newsecret"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await test_client.post(
        "/api/v1/users/token", data=urlencode(param), headers=headers
    )
    token = response.json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}
    response = await test_client.delete("/api/v1/users/deleteme", headers=h)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    user = await engine.find_one(User, User.email == "test2@email.com")
    assert user.active == False


async def test_get_users(
    test_client: TestClient, engine: AIOEngine, admin_token_header: dict
):
    response = await test_client.get("/api/v1/users/", headers=admin_token_header)
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_user(
    test_client: TestClient, engine: AIOEngine, admin_token_header: dict
):
    user = await engine.find(User)
    user_id = user[0].dict()["id"]
    username = user[0].dict()["username"]
    response = await test_client.get(
        f"/api/v1/users/{user_id}", headers=admin_token_header
    )
    assert response.status_code == 200
    data = response.json()["user"]
    assert data["username"] == username


async def test_patch_user(
    test_client: TestClient, engine: AIOEngine, admin_token_header: dict
):
    user = await engine.find_one(User, User.email == "test@email.com")
    user_id = user.id
    user_name = user.name
    response = await test_client.patch(
        f"/api/v1/users/{user_id}",
        json=dict(name="new name"),
        headers=admin_token_header,
    )
    assert response.status_code == 200
    user = await engine.find_one(User, User.id == user_id)
    assert user.name == "new name"
    assert user.name != user_name
    response = await test_client.patch(
        f"/api/v1/users/{user_id}",
        json=dict(name=user_name),
        headers=admin_token_header,
    )
    assert response.status_code == 200
    user = await engine.find_one(User, User.id == user_id)
    assert user.name == user_name


async def test_delete_user(
    test_client: TestClient, engine: AIOEngine, admin_token_header: dict
):
    user = await engine.find_one(User, User.email == "test@email.com")
    user_id = user.id
    response = await test_client.delete(
        f"/api/v1/users/{user_id}", headers=admin_token_header
    )
    assert response.status_code == 200
    soft_deleted = await engine.find_one(User, User.email == "test@email.com")
    assert soft_deleted.active == False
