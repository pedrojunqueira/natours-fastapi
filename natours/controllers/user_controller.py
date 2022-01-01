from typing import List
from pathlib import Path
import uuid

import aiofiles
from PIL import Image
from fastapi.exceptions import HTTPException
from odmantic import ObjectId

from natours.models.database import engine as db
from natours.models.user_model import User

authentication_fields = [
    "username",
    "role" "password",
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
    user.active = False

    await db.save(user)

    return user


async def get_users():
    users = await db.find(User)
    return [select_user_keys(user) for user in users]


async def get_user(Id: str):
    user = await db.find_one(User, User.id == ObjectId(Id))
    if not user:
        raise HTTPException(404, "cannot find user by Id")
    return select_user_keys(user)


async def delete_user(Id):
    user = await db.find_one(User, User.id == ObjectId(Id))
    if not user:
        raise HTTPException(404, "cannot find user by Id")
    if user:
        user.active = False
        await db.save(user)
    return user


def select_user_keys(
    user: User, keys: List = ["username", "name", "email", "lastname", "role", "photo"]
):
    return_user = {}
    return_user["id"] = f"{user.dict()['id']}"
    for k, v in user.dict().items():
        if k in keys:
            return_user[k] = v
    return return_user


p = Path(__file__).parent.resolve().parent / "public/img/users"


async def resize_picture(file_path):
    output_size = (125, 125)
    i = Image.open(file_path)
    i.thumbnail(output_size)
    i.save(file_path)


def check_image_ext(path):
    return path.suffix in [".png", ".jpeg", ".jpg", ".tif"]


def delete_old_photo_file(file):
    if not file:
        return
    path = p / file
    try:
        path.unlink()
    except OSError as err:
        print(err)


async def update_user_photo_name(user, photo_name):
    current_photo = user.photo
    delete_old_photo_file(current_photo)
    user.photo = photo_name
    await db.save(user)


async def upload_image(file, user):
    file_suffix = uuid.uuid4().hex
    file_path = p / f"user-{file_suffix}{Path(file.filename).suffix}"
    user_photo_name = file_path.name
    await update_user_photo_name(user, user_photo_name)
    if not check_image_ext(p / file.filename):
        raise HTTPException(
            404, "image file extention allowed only .png .jpg .jpeg .tif"
        )
    async with aiofiles.open(file_path, "wb") as fp:
        file_content = await file.read()
        await fp.write(file_content)
        await resize_picture(file_path)
    return file.filename
