from natours.models.user_model import Users
from natours.models.database import engine as db

async def signup(user):
    user = await db.save(user)
    return user.dict()