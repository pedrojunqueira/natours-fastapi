import pytest

from fastapi.testclient import TestClient

from natours.app import create_application

@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client
