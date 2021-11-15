import os
from functools import lru_cache

from fastapi import FastAPI, Request
from mongoengine import connect


from routes import tour_routes, user_routes
import config

app = FastAPI()


@lru_cache()
def get_settings():
    return config.Settings()


settings = get_settings()


@app.middleware("http")
async def add_some_middleware(request: Request, call_next):
    response = await call_next(request)
    print(f"hello from middleware 🧸")
    return response


app.include_router(tour_routes.router, prefix="/api/v1/tours", tags=["tours"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
def heart_beat():
    return {"I ❤️ FastAPI": "🙋🏽‍♂️"}


@app.on_event("startup")
async def startup_event():
    if settings.FASTAPI_ENV == "development":
        connect(host=settings.DATABASE_LOCAL)
        print("connected to Local DB")
    if settings.FASTAPI_ENV == "production":
        connect(
            host=settings.DATABASE.replace("<password>", settings.DATABASE_PASSWORD)
        )
        print("connected to PROD DB")
