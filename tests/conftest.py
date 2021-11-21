import pytest
import os

from fastapi.testclient import TestClient

from natours.app import create_application
from natours.config import Settings, get_settings

def get_settings_override():
    return Settings(FASTAPI_ENV="development", DATABASE_LOCAL="mongodb://localhost:27017/natoursfastapi")


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client
