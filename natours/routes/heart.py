import fastapi
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

router = fastapi.APIRouter()

limiter = Limiter(key_func=get_remote_address)

@router.get("/")
@limiter.limit("5/minute")
async def heart_beat(request: Request):

    return {"I ❤️ FastAPI": "🙋🏽‍♂️"}
