from os import wait
import fastapi
from fastapi import Response, status, Request

from controllers import tour_controller
from models.tour_model import Tours

router = fastapi.APIRouter()


@router.get("/")
async def get_all_tours():
    tours = await tour_controller.get_tours()
    return {
        "status": "success",
        "results": len(tours),
        "data": tours,
    }


@router.post("/")
async def create_tour(tour: Tours):
    tour = await tour_controller.post(tour)
    return {
        "status": "success",
        "data": {
            "tour": tour,
        },
    }


@router.get("/{Id:str}")
async def get_tour(Id: str, response: Response):
    tour = await tour_controller.get_tour(Id)
    if tour:
        return {
            "status": "success",
            "data": tour,
        }
    if not tour:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "fail", "message": "Invalid Id"}


@router.patch("/{Id:str}")
async def update_tour(tour:Tours, Id: str):
    tour = await tour_controller.patch_tour(Id, tour)
    return {
        "status": "success",
        "tour updated to": tour,
    }


@router.delete("/{Id:str}")
async def delete_tour(Id: str):
    tour = await tour_controller.delete_tour(Id)
    return {
        "status": "success",
        "tour deleted": tour,
    }
