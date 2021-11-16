from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from config import settings

client = AsyncIOMotorClient(settings.DATABASE_LOCAL)

if settings.FASTAPI_ENV == "production":
    client = AsyncIOMotorClient(settings.DATABASE.replace("<password>", settings.DATABASE_PASSWORD))

engine = AIOEngine(motor_client=client, database="natoursfastapi")
