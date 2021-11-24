import fastapi

router = fastapi.APIRouter()


@router.get("/")
async def heart_beat():

    return {"I ❤️ FastAPI": "🙋🏽‍♂️"}

