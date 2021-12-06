from typing import List

from fastapi.exceptions import HTTPException
from odmantic import ObjectId

from natours.models.database import engine as db
from natours.models.user_model import User

authentication_fields = [
    "username",
    "email",
    "password",
    "confirm_password",
    "password_changed_at",
    "password_reset_token",
    "password_reset_expire",
]


def validate_patch_body(patch, model):
    keys = patch.keys()
    model_keys = model.dict().keys()
    if any(k in authentication_fields for k in keys):
        raise HTTPException(401, "cannot update authentication field")
    return all(k in model_keys for k in keys)


async def patch_user(user_patch: dict, current_user: User):
    user = current_user
    if validate_patch_body(user_patch, user):
        for k, v in user_patch.items():
            if k != "id":
                setattr(user, k, v)
        await db.save(user)
    return user_patch


async def delete_me(user):
    user.disabled = True

    await db.save(user)

    return user


async def get_users():
    users = await db.find(User)
    return [select_user_keys(user) for user in users]


async def get_user(Id: str):
    user = await db.find_one(User, User.id == ObjectId(Id))
    if not user:
        raise HTTPException(404, "cannot find user by Id")
    return user


async def delete_user(Id):
    user = await db.find_one(User, User.id == ObjectId(Id))
    if not user:
        raise HTTPException(404, "cannot find user by Id")
    if user:
        await db.delete(user)
    return user


def select_user_keys(user: User, keys: List = ["name", "lastname", "email", "createdAt"]):
    return_user = user
    response = {k:v for k, v in return_user.dict().items() if k in keys}
    return response
