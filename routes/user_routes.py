import fastapi

router = fastapi.APIRouter()

@router.get('/api/v1/users')
async def get_all_users():
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }


@router.post('/api/v1/users')
async def create_user(tour:dict):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }

@router.get('/api/v1/users/{id:int}')
async def get_user(id:int):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }


@router.patch('/api/v1/users/{id:int}')
async def update_user(id:int):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }

@router.delete('/api/v1/users/{id:int}')
async def delete_user(id:int):
    return {
        "status" : 'error',
        "message" : 'not yet implemented'   }
