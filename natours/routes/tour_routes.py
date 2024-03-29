import fastapi
from fastapi import Body, HTTPException, Request, Security
from fastapi.param_functions import Depends
from odmantic import ObjectId

from natours.controllers import tour_controller, user_controller, review_controller
from natours.controllers import authentication_controller
from natours.models.tour_model import Tour
from natours.models.user_model import User
from natours.models.review_model import Review


router = fastapi.APIRouter()


@router.get("/tour-stats")
async def get_tour_stats():
    stats = await tour_controller.tour_stats()
    return {"tour stats": stats}


@router.get("/monthly-plan/{year:int}")
async def monthly_plan(year: int):
    plan = await tour_controller.get_monthly_plan(year)
    return {f"year plan for {year}": plan}


@router.get("/")
async def get_all_tours(
    request: Request,
    page: int = 1,
    limit: int = 100,
):

    query = request.query_params._dict
    tours = await tour_controller.get_tours(query)
    return {
        "status": "success",
        "results": len(tours),
        "data": tours,
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


## secure all CUD routes

admin_resource = authentication_controller.RoleChecker(["admin", "lead-guide"])


@router.post("/", dependencies=[Depends(admin_resource)])
async def create_tour(
    tour: Tour,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    tour = await tour_controller.post(tour)
    return {
        "status": "success",
        "data": {
            "tour": tour,
        },
    }


@router.patch("/{Id:str}", dependencies=[Depends(admin_resource)])
async def update_tour(
    Id: ObjectId,
    tour_patch: dict = Body(...),
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    tour = await tour_controller.patch_tour(Id, tour_patch)
    if not tour:
        raise HTTPException(404, "could not find item")
    if tour:
        return {
            "status": "success",
            "tour updated to": tour,
        }


@router.delete("/{Id:str}", dependencies=[Depends(admin_resource)])
async def delete_tour(
    Id: ObjectId,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    tour = await tour_controller.delete_tour(Id)
    if not tour:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "tour deleted": tour,
    }


@router.get("/{Id:str}/reviews")
async def create_tour_reviews(
    Id: str,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    reviews = await review_controller.get_tour_reviews(Id)
    return {
        "status": "success",
        "data": {
            "reviews": reviews,
        },
    }


@router.post("/{Id:str}/reviews")
async def create_review(
    review: Review,
    Id: str,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    tour = await tour_controller.get_tour(Id)
    review = await review_controller.post_review(
        review=review, user=current_user, tour=tour
    )
    return {
        "status": "success",
        "data": {
            "review added": review,
        },
    }
