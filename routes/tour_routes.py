import fastapi
from fastapi import Response, status, Request

from controllers import tour_controller

router = fastapi.APIRouter()


@router.get("/")
async def get_all_tours():
    tours = tour_controller.get_tours()
    return {
        "status": "success",
        "results": len(tours),
        "data": tours,
    }


@router.post("/")
async def create_tour(tour: dict):
    tour = tour_controller.post(tour)
    return {
        "status": "success",
        "data": {
            "tour": tour,
        },
    }


@router.get("/{Id:int}")
async def get_tour(Id: int, response: Response):
    tour = tour_controller.get_tour(Id)
    if tour:
        return {
            "status": "success",
            "data": tour[0],
        }
    if not tour:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "fail", "message": "Invalid Id"}


@router.patch("/{Id:int}")
async def update_tour(Id: int):
    return {
        "status": "success",
        "data": None,
    }


@router.delete("/{Id:int}")
async def delete_tour(Id: int):
    return {
        "status": "success",
        "data": None,
    }
