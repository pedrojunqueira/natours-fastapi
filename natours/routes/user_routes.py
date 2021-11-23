from sys import implementation
import fastapi


from natours.models.user_model import Users
from natours.controllers import authentication_controller

router = fastapi.APIRouter()


@router.post("/signup")
async def sign_up(user: Users):
    user = await authentication_controller.signup(user)

    return {"status": "success", "data": user}

@router.post("/login")
async def log_in():
    return {"status": "error", "message": "not yet implemented"}

@router.get("/")
async def get_all_users():
    return {"status": "error", "message": "not yet implemented"}


@router.post("/")
async def create_user(tour: dict):
    return {"status": "error", "message": "not yet implemented"}


@router.get("/{id:int}")
async def get_user(id: int):
    return {"status": "error", "message": "not yet implemented"}


@router.patch("/{id:int}")
async def update_user(id: int):
    return {"status": "error", "message": "not yet implemented"}


@router.delete("/{id:int}")
async def delete_user(id: int):
    return {"status": "error", "message": "not yet implemented"}
