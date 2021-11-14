import fastapi

router = fastapi.APIRouter()


@router.get("/")
async def get_all_users():
    return {"status": "error", "message": "not yet implemented"}


@router.post("/")
async def create_user(tour: dict):
    return {"status": "error", "message": "not yet implemented"}


@router.get("/{id:int}")
async def get_user(id: int):
    return {"status": "error", "message": "not yet implemented"}


@router.patch("/{id:int}")
async def update_user(id: int):
    return {"status": "error", "message": "not yet implemented"}


@router.delete("/{id:int}")
async def delete_user(id: int):
    return {"status": "error", "message": "not yet implemented"}
