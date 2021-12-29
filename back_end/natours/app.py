from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

from natours.routes import heart, tour_routes, user_routes, review_routes

limiter = Limiter(key_func=get_remote_address)


origins = ["http://localhost:8080", "http://192.168.1.103:8080", "localhost:8080"]


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
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = create_application()
