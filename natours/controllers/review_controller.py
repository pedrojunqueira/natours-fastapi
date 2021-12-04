from datetime import datetime
from natours.models.tour_model import Tour

from fastapi.exceptions import HTTPException
from odmantic import ObjectId

from natours.models.database import engine as db
from natours.models.review_model import Review
from natours.models.user_model import User


async def get_reviews():
    reviews = await db.find(Review)
    return reviews


async def get_review(Id):
    review = await db.find_one(Review, Review.id == ObjectId(Id))
    if not review:
        raise HTTPException(404, "cannot find review by Id")
    return review


async def post_review(review: Review, user: User = None, tour: Tour = None):
    if not user and not tour:
        review = await db.save(review)
    review.user = user.id
    review.tour = tour.id
    review = await db.save(review)
    return review


async def delete_review(Id):
    review = await db.find_one(Review, Review.id == ObjectId(Id))
    if not review:
        raise HTTPException(404, "cannot find review by Id")
    if review:
        await db.delete(review)
    return review


async def get_tour_reviews(Id):
    reviews = await db.find(Review, Review.tour == ObjectId(Id))
    return reviews
