from datetime import timedelta

import fastapi
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from natours.config import settings
from natours.controllers import authentication_controller
from natours.controllers import email_controller
from natours.models.security_model import (
    EmailSchema,
    PasswordSchema,
    Token,
    UpdatePasswordSchema,
)
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
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(
    current_user: Users = Security(
        authentication_controller.get_current_user, scopes=["me"]
    )
):
    response = {
        "username": current_user.username,
        "email": current_user.email,
        "full name": f"{current_user.name if current_user.name else ''} {current_user.lastname if current_user.lastname else ''}",
    }

    return response


@router.post("/forgotpassword")
async def forgot_password(email: EmailSchema, request: Request):
    address = email.email

    token = await authentication_controller.save_reset_password_token_to_db(address)

    reset_url = f"{request.base_url}api/v1/users/resetpassword/{token}"

    html = email_controller.render_email_message(reset_url)

    await email_controller.send_password_reset_email(address, html)

    return {"status": "success", "message": f"email sent to {address} "}


@router.patch("/resetpassword/{token:str}")
async def reset_password(token: str, new_passwords: PasswordSchema):

    user = await authentication_controller.get_token_user(token)

    await authentication_controller.save_reset_password(user, new_passwords)

    # log the user in TODO

    await email_controller.send_password_reset_confirmation(user.email)

    return {"status": "success", "message": "your password was successfull reset"}


@router.patch("/updatemypassword")
async def update_my_password(
    passwords: UpdatePasswordSchema,
    current_user: Users = Security(
        authentication_controller.get_current_user, scopes=["me"]
    ),
):

    if not  authentication_controller.verify_password(passwords.current_password, current_user.password):
        raise HTTPException(404, f"current password is incorrect")

    user = await authentication_controller.save_updated_password(current_user, passwords)

    await email_controller.send_password_reset_confirmation(user.email)

    return {"status": "success", "message": f"password successfully updated for {user.email}"}


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
