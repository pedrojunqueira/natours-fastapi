import fastapi
from fastapi import HTTPException
from odmantic import ObjectId

from natours.controllers import review_controller
from natours.models.review_model import Review


router = fastapi.APIRouter()


@router.get("/")
async def get_all_reviews():
    reviews = await review_controller.get_reviews()
    return {
        "status": "success",
        "results": len(reviews),
        "data": reviews,
    }

@router.post("/")
async def create_review(review: Review):
    review = await review_controller.post_review(review)
    return {
        "status": "success",
        "data": {
            "review added": review,
        },
    }


@router.delete("/{Id:str}")
async def delete_review(Id: ObjectId):
    review = await review_controller.delete_review(Id)
    if not review:
        raise HTTPException(404, "could not find item")
    return {
        "status": "success",
        "review deleted": review,
    }
