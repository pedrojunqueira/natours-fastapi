from async_asgi_testclient import TestClient

import pytest

@pytest.mark.asyncio
async def test_quart_app():
    from natours.app import app

    async with TestClient(app) as client:
        resp = await client.get("/")
        assert resp.status_code == 200

        # resp = await client.get("/api/v1/tours/")
        # assert resp.status_code == 200
        