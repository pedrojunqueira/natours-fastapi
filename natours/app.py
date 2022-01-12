import logging
import time
import random
import string

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from natours.routes import heart, tour_routes, user_routes, review_routes
from natours.config import settings

limiter = Limiter(key_func=get_remote_address)

origins = ["*"]

origins = settings.CORS_ORIGINS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('./logs/main.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("application stated")

    return application


app = create_application()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code} host={request.client.host}")
    
    return response