from datetime import datetime, timedelta

import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from natours.config import settings
from natours.controllers import authentication_controller
from natours.models.security_model import Token
from natours.models.user_model import Users

router = fastapi.APIRouter()


@router.post("/signup")
async def sign_up(user: Users):
    verified_non_existing_user = (
        await authentication_controller.verify_non_existing_user(user)
    )
    if verified_non_existing_user:
        created_user = await authentication_controller.signup(user)
        return {"status": "success", "data": created_user}
    else:
        raise HTTPException(404, f"email or user already exist")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authentication_controller.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication_controller.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=Users)
async def read_users_me(
    current_user: Users = Depends(authentication_controller.get_current_user),
):
    return current_user


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
