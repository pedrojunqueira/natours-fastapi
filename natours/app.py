from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from natours.routes import heart, tour_routes, user_routes, review_routes

limiter = Limiter(key_func=get_remote_address)


def create_application() -> FastAPI:
    application = FastAPI()
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.include_router(
        tour_routes.router, prefix="/api/v1/tours", tags=["tours"]
    )
    application.include_router(
        user_routes.router, prefix="/api/v1/users", tags=["users"]
    )
    application.include_router(
        review_routes.router, prefix="/api/v1/reviews", tags=["reviews"]
    )
    application.include_router(heart.router)

    return application


app = create_application()


# @app.middleware("http")
# async def add_some_middleware(request: Request, call_next):
#     response = await call_next(request)
#     print(f"hello from middleware 🧸")
#     return response
