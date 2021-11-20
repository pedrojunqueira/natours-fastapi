import fastapi
from fastapi import Response, status, Request, Body, HTTPException
from odmantic import ObjectId

from controllers import tour_controller
from models.tour_model import Tours

router = fastapi.APIRouter()


@router.get("/tour-stats")
async def get_tour_stats():
    stats = await tour_controller.tour_stats()
    return {"tour stats": stats }


@router.get("/monthly-plan/{year:int}")
async def monthly_plan(year:int):
    plan = await tour_controller.get_monthly_plan(year)
    return {f"year plan for {year}": plan }


@router.get("/")
async def get_all_tours(request: Request, page: int = 1, limit: int = 100):
    query = request.query_params._dict
    tours = await tour_controller.get_tours(query)
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
async def get_tour(Id: ObjectId):
    tour = await tour_controller.get_tour(Id)
    if not tour:
        raise HTTPException(404, "could not find item")
    if tour:
        return {
            "status": "success",
            "data": tour,
        }


@router.patch("/{Id:str}")
async def update_tour(Id: ObjectId, tour_patch: dict = Body(...)):
    tour = await tour_controller.patch_tour(Id, tour_patch)
    if not tour:
        raise HTTPException(404, "could not find item")
    if tour:
        return {
        "status": "success",
        "tour updated to": tour,
            }
    
       
@router.delete("/{Id:str}")
async def delete_tour(Id: ObjectId):
    tour = await tour_controller.delete_tour(Id)
    if not tour:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "tour deleted": tour,
    }


