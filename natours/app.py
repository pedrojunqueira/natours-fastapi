from fastapi import FastAPI, Request
from natours.routes import tour_routes, user_routes, heart


app = FastAPI()


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(
        tour_routes.router, prefix="/api/v1/tours", tags=["tours"]
    )
    application.include_router(
        user_routes.router, prefix="/api/v1/users", tags=["users"]
    )
    application.include_router(heart.router)

    return application


app = create_application()


@app.middleware("http")
async def add_some_middleware(request: Request, call_next):
    response = await call_next(request)
    print(f"hello from middleware 🧸")
    return response

