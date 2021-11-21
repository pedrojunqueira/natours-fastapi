

def test_heart_beat(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"I ❤️ FastAPI": "🙋🏽‍♂️"}
