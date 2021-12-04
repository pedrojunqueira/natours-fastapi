import fastapi
from fastapi import HTTPException, Depends
from odmantic import ObjectId

from natours.controllers import review_controller, authentication_controller
from natours.models.review_model import Review
from natours.models.user_model import User

router = fastapi.APIRouter()


@router.get("/")
async def get_all_reviews():
    reviews = await review_controller.get_reviews()
    return {
        "status": "success",
        "results": len(reviews),
        "data": reviews,
    }


@router.get("/{Id:str}")
async def get_reviews(
    Id: ObjectId,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    reviews = await review_controller.get_review(Id)
    return {
        "status": "success",
        "results": len(reviews.dict()),
        "data": reviews,
    }


admin_resource = authentication_controller.RoleChecker(["admin"])


@router.delete("/{Id:str}", dependencies=[Depends(admin_resource)])
async def delete_review(
    Id: ObjectId,
    current_user: User = Depends(authentication_controller.get_current_active_user),
):
    review = await review_controller.delete_review(Id)
    if not review:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "review deleted": review,
    }
