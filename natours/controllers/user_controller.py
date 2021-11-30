
from fastapi.exceptions import HTTPException
from natours.models.database import engine as db

authentication_fields = ["username",
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

async def patch_user(current_user, user_patch):
    user = current_user
    if validate_patch_body(user_patch, user):
        for k, v in user_patch.items():
            if k != "id":
                setattr(user, k, v)
        await db.save(user)
    return user_patch


async def delete_me(user):
    # soft delete user by marking if inactive
    user.disabled = True
    
    await db.save(user)

    return user