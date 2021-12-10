async def test_update_me(test_client: TestClient, test_token_header: dict, engine:AIOEngine):
    user = await engine.find_one(User, User.email == "test2@email.com")
    # assert user.name == None
    # assert user.lastname == None
    print(user)
    body =    {
        "name": "test_name",
        "lastname": "test_lastname",
        }       
    response = await test_client.patch("/api/v1/users/updateme", headers=test_token_header, json=body)
    print(response.json())
    # assert response.status_code == 200
    # assert response.json()["status"] == "success"
    # user = await engine.find_one(User, User.email == "test2@email.com")
    # assert user.name == body["name"]
    # assert user.lastname == body["lastname"]
