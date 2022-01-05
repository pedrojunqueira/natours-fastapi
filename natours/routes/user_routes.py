from datetime import timedelta
from typing import List

import fastapi
from fastapi import (
    Depends,
    HTTPException,
    status,
    Body,
    Request,
    Response,
    File,
    UploadFile,
)
from fastapi.security import OAuth2PasswordRequestForm

from natours.config import settings
from natours.controllers import (
    authentication_controller,
    azure_blob_controller,
    user_controller,
    email_controller,
)
from natours.models.security_model import (
    EmailSchema,
    PasswordSchema,
    Token,
    UpdatePasswordSchema,
)
from natours.models.user_model import User

router = fastapi.APIRouter()


@router.post("/signup")
async def sign_up(user: User):
    verified_non_existing_user = (
        await authentication_controller.verify_non_existing_user(user)
    )
    if verified_non_existing_user:
        created_user = await authentication_controller.signup(user)
        response = user_controller.select_user_keys(created_user)
        return {"status": "success", "data": response}
    else:
        raise HTTPException(404, f"email or user already exist")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
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
    # response.set_cookie(
    #     key="jwt",
    #     value=access_token,
    #     expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    #     httponly=True,
    # )
    return {"access_token": access_token, "token_type": "bearer"}


allow_cud_resource = authentication_controller.RoleChecker(["admin"])


@router.get("/me")
async def read_users_me(
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    response = user_controller.select_user_keys(current_user)
    return response


@router.post("/forgotpassword")
async def forgot_password(email: EmailSchema, request: Request):
    address = email.email

    token = await authentication_controller.save_reset_password_token_to_db(address)

    reset_url = f"{settings.RESET_PASSWORD_REDIRECT}/{token}"

    html = email_controller.render_email_message(reset_url)

    await email_controller.send_password_reset_email(address, html)

    return {"status": "success", "message": f"email sent to {address} "}


@router.patch("/resetpassword/{token:str}")
async def reset_password(token: str, new_passwords: PasswordSchema):

    user = await authentication_controller.get_token_user(token)

    await authentication_controller.save_reset_password(user, new_passwords)

    await email_controller.send_password_reset_confirmation(user.email)

    # log the user in TODO

    return {"status": "success", "message": "your password was successfull reset"}


@router.patch("/updatemypassword")
async def update_my_password(
    passwords: UpdatePasswordSchema,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):

    if not authentication_controller.verify_password(
        passwords.current_password, current_user.password
    ):
        raise HTTPException(404, f"current password is incorrect")

    user = await authentication_controller.save_updated_password(
        current_user, passwords
    )

    await email_controller.send_password_reset_confirmation(user.email)

    # log the user in TODO

    return {
        "status": "success",
        "message": f"password successfully updated for {user.email}",
    }


@router.patch("/updateme")
async def update_me(
    current_user: User = Depends(authentication_controller.get_current_active_user),
    user_patch: dict = Body(...),
):

    user = await user_controller.patch_user(user_patch, current_user)

    return {"status": "success", "data updated for user": user}


@router.delete("/deleteme")
async def delete_me(
    current_user: User = Depends(authentication_controller.get_current_active_user),
):

    user = await user_controller.delete_me(current_user)

    return {
        "status": "success",
        "message": f"user {user.username} successfully deleted",
    }


@router.get("/{Id:str}")
async def get_user(
    Id: str,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    user = await user_controller.get_user(Id)
    return {"status": "success", "user": user}


@router.post("/upload_user_image/")
async def create_upload_files(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    file = await azure_blob_controller.upload_image_to_blob(files[0], current_user)
    return {"message": f"{file} uploaded successfully"}


## secure all CUD routes

admin_resource = authentication_controller.RoleChecker(["admin"])


@router.get("/", dependencies=[Depends(admin_resource)])
async def get_all_users(
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    users = await user_controller.get_users()
    return {"status": "success", "users": users}


@router.patch("/{Id:str}", dependencies=[Depends(admin_resource)])
async def update_user(
    Id: str,
    current_user: User = Depends(authentication_controller.get_current_active_user),
    user_patch: dict = Body(...),
):
    user_to_patch = await user_controller.get_user(Id)
    user = await user_controller.patch_user(user_patch, user_to_patch)
    return {"status": "success", "user updated": user}


@router.delete("/{Id:str}", dependencies=[Depends(admin_resource)])
async def delete_user(
    Id: str,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    user = await user_controller.delete_user(Id)
    return {"status": "user", "user deleted": user}
